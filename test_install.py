"""Installer checks use isolated temporary directories; no real Codex data."""
from pathlib import Path
import shutil
import tempfile
import unittest
from install import install, FILES, PET_ID

SOURCE = Path(__file__).resolve().parent


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / 'Codex data with spaces'

    def test_dry_run_writes_nothing(self):
        install(SOURCE, self.home, dry_run=True)
        self.assertFalse(self.home.exists())

    def test_install_and_repeat_are_idempotent(self):
        destination = install(SOURCE, self.home)
        for name in FILES:
            self.assertEqual((destination / name).read_bytes(), (SOURCE / name).read_bytes())
        install(SOURCE, self.home)
        self.assertFalse((self.home / 'pets/.backups').exists())

    def test_update_backs_up_old_files_and_preserves_unrelated_files(self):
        destination = self.home / 'pets' / PET_ID
        destination.mkdir(parents=True)
        (destination / 'spritesheet.webp').write_bytes(b'old artwork')
        (destination / 'notes.txt').write_text('keep me')
        install(SOURCE, self.home)
        backups = list((self.home / 'pets/.backups').glob('*/spritesheet.webp'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), b'old artwork')
        self.assertEqual((destination / 'notes.txt').read_text(), 'keep me')

    def test_invalid_checksum_never_writes_destination(self):
        bad = self.root / 'bad'; bad.mkdir()
        for name in (*FILES, 'SHA256SUMS'):
            shutil.copy2(SOURCE / name, bad / name)
        (bad / 'spritesheet.webp').write_bytes(b'corrupt')
        with self.assertRaises(ValueError):
            install(bad, self.home)
        self.assertFalse(self.home.exists())

    def test_directory_symlink_is_rejected(self):
        other = self.root / 'other'; other.mkdir()
        pets = self.home / 'pets'; pets.mkdir(parents=True)
        try:
            (pets / PET_ID).symlink_to(other, target_is_directory=True)
        except OSError:
            self.skipTest('Symlink creation unavailable')
        with self.assertRaises(ValueError):
            install(SOURCE, self.home)
        self.assertEqual(list(other.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
