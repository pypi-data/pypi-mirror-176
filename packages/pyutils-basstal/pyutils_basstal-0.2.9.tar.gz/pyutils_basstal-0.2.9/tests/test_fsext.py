import shutil
import unittest
import pyutils.fsext as fs
import os


class TestFsext(unittest.TestCase):

    def setUp(self) -> None:
        self.test_root_dir = os.path.dirname(__file__)
        return super().setUp()

    def test_to_base64(self):
        cwd = os.getcwd()
        if not cwd.endswith('tests'):
            os.chdir('tests')
        self.assertEqual(fs.to_base64('abs'), '')
        self.assertNotEqual(fs.to_base64('./data/to_base64.png'), '')
        output_dir = './output'
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        output_file = os.path.join(output_dir, 'to_base64')
        content = fs.to_base64('./data/to_base64.png', output_file)
        with open(output_file, 'r+', encoding='utf-8') as f:
            self.assertEqual(f.readline(), content)

    def test_convert_encoding(self):
        with open(os.path.join(self.test_root_dir, 'data/test_convert_encoding'), 'rb') as f:
            test_convert_encoding = f.read()
        gbk_encoding_source_path = os.path.join(self.test_root_dir, "data/gbk_encoding")
        test_gbk_encoding_path = os.path.join(os.path.dirname(gbk_encoding_source_path), 'test_gbk_encoding')
        shutil.copyfile(gbk_encoding_source_path, test_gbk_encoding_path)
        with open(test_gbk_encoding_path, 'rb') as f:
            gbk_encoding = f.read()
        self.assertNotEqual(gbk_encoding, test_convert_encoding)
        fs.convert_encoding(test_gbk_encoding_path)
        with open(test_gbk_encoding_path, 'rb') as f:
            gbk_encoding = f.read()
        self.assertEqual(gbk_encoding, test_convert_encoding)

    def test_copy_files(self):
        """copy_files 将目标文件列表中的文件复制到目标文件夹下，目标文件列表可以包含文件或文件夹。
        """
        # 测试 copy 简单的文件 和 文件夹
        target_path = os.path.join(self.test_root_dir, 'data/copy_test')
        source_dir = os.path.join(target_path, 'source')
        source_list = [os.path.join(source_dir, filename) for filename in os.listdir(source_dir)]

        fs.copy_files(target_path, source_list)
        filenames = [filename for filename in os.listdir(source_dir)]
        for filename in filenames:
            self.assertTrue(os.path.exists(os.path.join(target_path, filename)))

        # 测试 覆盖 的效果
        test_copy_file_path = os.path.join(target_path, 'test_copy_file')
        with open(test_copy_file_path, 'w+') as f:
            f.write('add more info')
        fs.copy_files(target_path, source_list)
        with open(test_copy_file_path, 'r+') as f:
            lines = f.readlines()
        content = '\n'.join(lines)
        self.assertTrue('add more info' not in content)
