from setuptools import setup, find_packages

setup(
    name = "python_monitor",      #这里是pip项目发布的名称
    version = "0.0.2",  #版本号，数值大的会优先被pip
    keywords = ["pip", "python_monitor"],			# 关键字
    description = "monitor your python process",	# 描述
    long_description = "monitor your python process",
    license = "MIT Licence",		# 许可证

    url = "https://github.com/Dignn/python_monitor",     #项目相关文件地址，一般是github项目地址即可
    author = "zhangxiao",			# 作者
    author_email = "likezx@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["prometheus_client"]          #这个项目依赖的第三方库
)



