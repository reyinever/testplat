import os

# 每页显示的数据条数
per_page_rows=2

# 当前文件所在的目录
this_file_dir_path=os.path.dirname(os.path.abspath(__file__))
# 日志配置文件的路径
log_conf_path=os.path.join(this_file_dir_path,'Logger.conf')

# 唯一数 保存的文件
unique_number_path=os.path.join(this_file_dir_path,'unique_number.txt')

# html报告保存的路径
html_report_path=os.path.join(os.path.dirname(this_file_dir_path),'templates\\report\\testReport')

if __name__ == '__main__':
    # print(log_conf_path)
    # print(unique_number_path)
    print(html_report_path)