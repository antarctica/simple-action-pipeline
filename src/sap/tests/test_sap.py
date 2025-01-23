# test_sap.py

import unittest
import shutil, os
from unittest.mock import patch
#from io import StringIO
from contextlib import contextmanager

import sap.pipeline as pipeline
from pathlib import Path


class TestCLI(unittest.TestCase):
    """Test the cli user functionality"""

    ## Get the full path of this test file
    test_file_path = Path(__file__).parent.absolute()
    ## Get the valid example pipeline path
    pipeline_path = list(test_file_path.parents)[2]

    #@patch('sys.stdout', new_callable=StringIO)
    #@patch('sys.stderr', new_callable=StringIO)
    #def test_unknown_pipeline_directory(self, mock_stderr, mock_stdout):
    #    with patch("sys.argv", ["_", "status", str(self.test_file_path)]):
    #        pipeline.main()
    #        stdout_value = mock_stdout.getvalue()
    #        stderr_value = mock_stderr.getvalue()
    #        self.assertEqual(stdout_value, "This is a message to stdout.\n")


                
    
    def test_pipeline_status(self):
        """test of the status action which determines the status of any pipeline directory"""
        ## test an 'unknown' directory
        self.assertEqual(pipeline.perform(str(self.pipeline_path), "status", False, False, False), "unknown")

        ## test an 'unbuilt' directory
        unbuilt_path = Path.joinpath(self.pipeline_path, 'example')
        try:
            shutil.rmtree(Path.joinpath(unbuilt_path, 'workflow-manager'))
            os.remove(Path.joinpath(unbuilt_path, 'pipeline.env'))
            os.remove(Path.joinpath(unbuilt_path, 'application.env'))
        except: pass
        self.assertEqual(pipeline.perform(str(unbuilt_path), "status", False, False, False), "unbuilt")

        ## test a 'built' directory
        pipeline.perform(str(unbuilt_path), "build", False, False, False)
        self.assertEqual(pipeline.perform(str(unbuilt_path), "status", False, False, False), "built")

        ## test a 'built' directory having been rebuilt with '--rebuild' option
        pipeline.perform(str(unbuilt_path), "build", True, False, False)
        self.assertEqual(pipeline.perform(str(unbuilt_path), "status", False, False, False), "built")

        ## test a 'built' directory with '--short' option
        self.assertEqual(pipeline.perform(str(unbuilt_path), "status", False, False, True), "built")

    def test_pipeline_build(self):
        """test of the build action which builds the pipeline from the provided configs"""
        ## test an 'unknown' directory
        pipeline.perform(str(self.pipeline_path), "build", False, False, False)
        self.assertEqual(pipeline.perform(str(self.pipeline_path), "status", False, False, False), "unknown")

        ## test an 'unbuilt' directory
        unbuilt_path = Path.joinpath(self.pipeline_path, 'example')
        try:
            shutil.rmtree(Path.joinpath(unbuilt_path, 'workflow-manager'))
            os.remove(Path.joinpath(unbuilt_path, 'pipeline.env'))
            os.remove(Path.joinpath(unbuilt_path, 'application.env'))
        except: pass
        self.assertEqual(pipeline.perform(str(unbuilt_path), "build", False, False, False), "unbuilt")

        # test a 'built' directory without the rebuild flag (user input == 'n')
        with patch('builtins.input', return_value='n'):
            self.assertEqual(pipeline.perform(str(unbuilt_path), "build", False, False, False), "built")
        
        # test a 'built' directory without the rebuild flag (user input == 'y')
        with patch('builtins.input', return_value='y'):
            self.assertEqual(pipeline.perform(str(unbuilt_path), "build", False, False, False), "built")
        
        # test a 'built' directory with the rebuild flag
        self.assertEqual(pipeline.perform(str(unbuilt_path), "build", True, False, False), "built")

    def test_pipeline_execute(self):
        """test the execution of a built pipeline"""
        with patch("sys.argv", ["_", "execute", str(Path.joinpath(self.pipeline_path, 'example'))]):
            pipeline.main()
        

    #def test_pipeline_cli(self):
    #    with patch("sys.argv", ["_", "status", str(Path.joinpath(self.pipeline_path, 'example'))]):
    #        returned = pipeline.main()

        #assert args.e is True
        #assert args.area_dict is None

if __name__ == '__main__':
    unittest.main(verbosity=2)