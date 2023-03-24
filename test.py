from fileutil.file_util import FileUtil
from shutil import copytree, ignore_patterns
# for i in FileUtil.list_target_files("commonutil", "py", use_abstract_path=False):
#     print(i)


FileUtil.copy_dir(".", 'E:\\temp\\test', ignore=['py'])