from os.path import join
from unittest import TestCase, main, mock

from tum_exam_scripts.main import app
from typer.testing import CliRunner


class SendAllTest(TestCase):
    """
    Send All Test
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = CliRunner()

    @mock.patch("typer.confirm")
    def test_send_all_broken_pdf(self, mock_typer):
        mock_typer.return_value = True

        result = self.runner.invoke(
            app,
            [
                "send-all-booklets",
                join("tests", "rsc", "exams_broken"),
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("0003-book.pdf is not a valid PDF", result.stdout)

    @mock.patch("typer.confirm")
    def test_send_all_empty_folder(self, mock_typer):
        mock_typer.return_value = True

        result = self.runner.invoke(
            app,
            [
                "send-all-booklets",
                join("tests", "rsc"),
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("We did not find any booklets.", result.stdout)

    @mock.patch("typer.confirm")
    def test_no_printing(self, mock_typer):
        mock_typer.return_value = False

        result = self.runner.invoke(
            app,
            [
                "send-all-booklets",
                join("tests", "rsc", "exams"),
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Please enable printing first", result.stdout)

    @mock.patch("typer.confirm")
    @mock.patch("subprocess.check_call")
    def test_send_all(
        self,
        mock_check_call,
        mock_typer,
    ):
        mock_typer.return_value = True
        mock_check_call.return_value = 0

        result = self.runner.invoke(
            app,
            [
                "send-all-booklets",
                join("tests", "rsc", "exams"),
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn('We found 2 booklets.', result.stdout)
        self.assertIn('Done!', result.stdout)

    @mock.patch("typer.confirm")
    @mock.patch("subprocess.check_call")
    def test_send_all_call_error(
            self,
            mock_check_call,
            mock_typer,
    ):
        mock_typer.return_value = True
        mock_check_call.return_value = 1

        result = self.runner.invoke(
                app,
                [
                    "send-all-booklets",
                    join("tests", "rsc", "exams"),
                ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn('We found 2 booklets.', result.stdout)
        self.assertIn('Something went wrong when sending', result.stdout)
        self.assertIn('E0001-book.pdf to the server', result.stdout)
        self.assertNotIn('Done!', result.stdout)

if __name__ == "__main__":
    main()
