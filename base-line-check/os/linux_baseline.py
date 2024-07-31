import os
import re
import subprocess

import schedule


def check_root():
    """检查脚本是否以 root 用户运行"""
    if os.geteuid() != 0:
        print("请以root用户身份运行此脚本")
        exit(1)


def run_command(command):
    """运行 shell 命令并返回输出"""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stderr.decode('utf-8')


# 身份鉴别
def check_user_group_settings():
    print("********************************")
    print("身份鉴别")
    print("********************************")
    not_allow = 0
    """
    应对登录操作系统和数据库系统的用户进行身份标识和鉴别
    1)操作系统使用口令鉴别机制对用户进行身份标识和鉴别；
    2)登录时提示输入用户名和口令；以错误口令或空口令登录时提示登录失败，验证了登录控制功能的有效性；
    3)操作系统不存在密码为空的用户
    """
    print('检查 登录操作系统和数据库系统的用户进行身份标识和鉴别')
    res2 = run_command("awk -F: '($3 == 0) { print $1 }' /etc/passwd")  # 操作系统 Linux 超级用户策略安全基线要求项
    if res2 != 'root\n':
        print("存在非root账号的账号UID为0的可疑帐号：不符合要求，请整改！")
        not_allow += 1
    else:
        print("不存在非root账号的账号UID为0的可疑帐号")
    res3 = run_command("awk -F: '($2 == \"\") {print}' /etc/shadow")
    if res3 == 0 or res3 == '!':
        print("存在空口令用户帐号，请查看该用户帐号是否危险！")
        not_allow += 1
    else:
        print("不存在空口令用户帐号")
    print("--------------------------------")

    """
    操作系统和数据库系统管理用户身份标识应具有不易被冒用的特点，口令应有复杂度要求并定期更换
    密码策略如下  PASS_MAX_DAYS   90（生命期最大为90天）
                PASS_MIN_DAYS   0（密码最短周期0天）
                PASS_MIN_LEN   10（密码最小长度10位）
                PASS_WARN_AGE 7（密码到期前7天提醒）
    口令复杂度：
    口令长度8位以上，并包含数字、字母、特殊字符三种形式
    """
    print('检查密码策略')
    pass_max = run_command("cat /etc/login.defs | grep PASS_MAX_DAYS | grep -v \"^#\" | awk '{print $2}'")
    pass_min = run_command("cat /etc/login.defs | grep PASS_MIN_DAYS | grep -v \"^#\" | awk '{print $2}'")
    pass_len = run_command("cat /etc/login.defs | grep PASS_MIN_LEN | grep -v \"^#\" | awk '{print $2}'")
    pass_age = run_command("cat /etc/login.defs | grep PASS_WARN_AGE | grep -v \"^#\" | awk '{print $2}'")
    if pass_max == '' or int(pass_max) <= 90:
        print('生命期最大应为90天')
    else:
        print('生命期最大为90天')
    if pass_min == '' or int(pass_min) > 0:
        print('密码最短周期应为0天')
    else:
        print('密码最短周期0天')
    if pass_len == '' or int(pass_len) < 10:
        print('密码最小长度应大于等于10位')
    else:
        print('密码最小长度10位')
    if pass_age == '' or int(pass_age) > 7:
        print('密码到期前7天应提醒')
    else:
        print('密码到期前7天提醒')
    print("--------------------------------")
    print("检查口令复杂度")
    try:
        with open('/etc/security/pwquality.conf', 'r') as file:
            content = file.read()
            minlen = re.search(r'^\s*minlen\s*=\s*(\d+)', content, re.MULTILINE)
            minclass = re.search(r'^\s*minclass\s*=\s*(\d+)', content, re.MULTILINE)
            if minlen and int(minlen.group(1)) >= 8:
                print("口令长度配置正确：至少8位")
            else:
                print("口令长度应至少8位")
            if minclass and int(minclass.group(1)) >= 2:
                print("口令复杂性配置正确：至少包含数字、大小写字母、特殊字符中的两种")
            else:
                print("口令复杂性配置错误，应包含数字、大小写字母、特殊字符中的两种")
    except FileNotFoundError:
        print("/etc/security/pwquality.conf 文件不存在")
    pam_files = ["/etc/pam.d/common-password", "/etc/pam.d/system-auth"]
    pwquality_enabled = False
    tag = 0
    for pam_file in pam_files:
        try:
            with open(pam_file, 'r') as file:
                content = file.read()
                if 'pam_pwquality.so' in content:
                    pwquality_enabled = True
                    break
        except FileNotFoundError:
            tag += 1
            continue
    if tag == 2:
        print("/etc/pam.d/common-password", '和', "/etc/pam.d/system-auth", "不存在")
    else:
        if pwquality_enabled:
            print("PAM 配置正确：启用了 pam_pwquality.so 模块")
        else:
            print("PAM 配置不正确：未启用 pam_pwquality.so 模块")
    print("--------------------------------")
    """
    应启用登录失败处理功能，可采取结束会话、限制非法登录次数和自动退出等措施
    1)操作系统已启用登陆失败处理、结束会话、限制非法登录次数等措施；
    2)当超过系统规定的非法登陆次数或时间登录操作系统时，系统锁定或自动断开连接
    """
    print("检查登录失败处理功能，PAM配置")
    pam_files = ["/etc/pam.d/common-auth", "/etc/pam.d/common-password"]
    for pam_file in pam_files:
        try:
            with open(pam_file, 'r') as file:
                content = file.read()
                if "pam_unix.so" in content or "pam_pwquality.so" in content:
                    print(f"{pam_file} 配置正确")
                else:
                    print(f"{pam_file} 配置缺失 pam_unix.so 或 pam_pwquality.so")
        except FileNotFoundError:
            print(f"{pam_file} 文件不存在")
    print("--------------------------------")
    """
    当对服务器进行远程管理时，应采取必要措施，防止鉴别信息在网络传输过程中被窃听
    1)操作系统使用SSH协议进行远程连接；
    2)若未使用SSH方式进行远程管理，则查看是否使用telnet方式进行远程管理；
    """
    print('SSH远程登录')
    res_ssh = run_command("service ssh status")
    if "not running" in res_ssh or 'not found' in res_ssh:
        print('未开启SSH远程连接')
        res_telnet = run_command("service telnet status")
        if 'not running' in res_telnet or 'unrecognized' in res_telnet or 'not found' in res_telnet:
            print("未开启telnet远程连接")
        else:
            print('已开启telnet远程连接')
    else:
        print('已开启SSH远程连接')
    print("--------------------------------")
    """
    为操作系统和数据库的不同用户分配不同的用户名，确保用户名具有唯一性
    若系统允许用户名相同，UID不同，则UID是唯一性标识；若系统允许UID相同，则用户名是唯一性标识
    """
    print('检查用户的标识唯一')
    try:
        with open('/etc/passwd', 'r') as file:
            lines = file.readlines()
            username_dict = {}
            uid_dict = {}
            for line in lines:
                parts = line.split(':')
                uid, username = parts[2], parts[0]
                if username in username_dict:
                    username_dict[username].append(uid)
                else:
                    username_dict[username] = [uid]
                if uid in uid_dict:
                    uid_dict[uid].append(username)
                else:
                    uid_dict[uid] = [username]
            # 检查相同用户名不同UID的情况
            username_conflicts = {k: v for k, v in username_dict.items() if len(v) > 1}
            if username_conflicts:
                print("存在相同用户名但不同UID的情况:")
                for username, uids in username_conflicts.items():
                    print(f"用户名: {username}, UID列表: {', '.join(uids)}")
            else:
                print("没有相同用户名但不同UID的情况")
            # 检查相同UID不同用户名的情况
            uid_conflicts = {k: v for k, v in uid_dict.items() if len(v) > 1}
            if uid_conflicts:
                print("存在相同UID但不同用户名的情况:")
                for uid, usernames in uid_conflicts.items():
                    print(f"UID: {uid}, 用户名列表: {', '.join(usernames)}")
            else:
                print("没有相同UID但不同用户名的情况")
    except FileNotFoundError:
        print("/etc/passwd 文件不存在")
    print("--------------------------------")


def check_view_control():
    print("********************************")
    print("访问控制")
    print("********************************")
    """
    应启用访问控制功能，依据安全策略控制用户对资源的访问
    r=4 w=2 x=1
    """
    files_to_check = ['/etc/passwd', '/etc/shadow', '/etc/group', '/etc/securetty', '/etc/services']
    for file in files_to_check:
        if os.path.exists(file):
            permissions = oct(os.stat(file).st_mode)[-3:]
            print(f"{file} 权限: {permissions}")
            if 'passwd' in file and permissions != 644:
                print(f"{file}权限不符合要求， root用户权限应为 644")
            if 'shadow' in file and permissions != 400:
                print(f"{file} 权限不符合要求，root用户权限应为 400")
            if 'group' in file and permissions != 644:
                print(f"{file} 权限不符合要求，root用户权限应为 644")
            if 'securetty' in file and permissions != 600:
                print(f"{file} 权限不符合要求，root用户权限应为 600")
            if 'services' in file and permissions != 644:
                print(f"{file} 权限不符合要求，root用户权限应为 644")
        else:
            print(f"{file} 文件不存在")
    print("--------------------------------")
    """
    应严格限制默认帐户的访问权限，重命名系统默认帐户，修改这些帐户的默认口令
    默认账户已更名，或已被禁用

    应及时删除多余的、过期的帐户，避免共享帐户的存在
    不存在多余、过期和共享账户
    
    查看 /etc/passwd
    """
    run_command('cat /etc/passwd')
    check_account = run_command('cat /etc/shadow |grep ^#')
    if check_account != "":
        print("存在多余账户")
    print("--------------------------------")


def check_security():
    print("********************************")
    print("安全审计")
    print("********************************")
    """
    审计范围应覆盖到服务器和重要客户端上的每个操作系统用户和数据库用户
    系统开启了安全审计功能或部署了第三方安全审计设备
    """
    open_auditd = False
    try:
        check_auditd = run_command("systemctl is-active auditd")
        if check_auditd == 'active':
            print("系统开启了安全审计功能")
            open_auditd = True
        else:
            print("系统未开启安全审计功能")
    except subprocess.CalledProcessError:
        print("系统没有 auditd 安全审计功能")
    third_party_services = [
        'rsyslog',  # 通用日志管理服务
        'splunkd',  # Splunk
        'wazuh-agent',  # Wazuh
        'ossec',  # OSSEC
        'falco',  # Falco
        'syslog-ng'  # Syslog-NG
    ]
    active_services = []
    inactive_services = []
    no_services = []
    for service in third_party_services:
        try:
            third_party_res = run_command("systemctl is-active " + service)
            print("systemctl is-active " + service, third_party_res)
            if third_party_res == 'active\n':
                active_services.append(service)
            elif third_party_res == "inactive\n":
                inactive_services.append(service)
        except subprocess.CalledProcessError:
            no_services.append(service)
            pass
    print("本次检查的第三方服务", third_party_services)
    print("已开启服务", active_services)
    print("未开启服务", inactive_services)
    print("未安装服务", no_services)
    """
    审计内容应包括重要用户行为、系统资源的异常使用和重要系统命令的使用等系统内重要的安全相关事件
    审计功能已开启，包括：用户的添加和删除、审计功能的启动和关闭、审计策略的调整、权限变更、系统资源的异常使用、重要的系统操作（如用户登录、退出）等设置
    """
    if open_auditd:
        print(run_command("cat /etc/audit/auditd.conf"))
        print(run_command("cat /etc/audit/audit.rules"))
    print("--------------------------------")

    """
    操作系统应遵循最小安装的原则，仅安装需要的组件和应用程序，并通过设置升级服务器等方式保持系统补丁及时得到更新
    1)系统安装的组件和应用程序遵循了最小安装的原则；
    2)不必要的服务没有启动；
    3)不必要的端口没有打开；
    """
    print("请检查正在运行的服务")
    print(run_command("service --status-all | grep 'running\|[+]'"))
    print("--------------------------------")


def check_source_control():
    print("********************************")
    print("资源控制")
    print("********************************")
    """
    应通过设定终端接入方式、网络地址范围等条件限制终端登录
    已设定终端登录安全策略及措施，非授权终端无法登录管理
    中对终端登录限制的相关配置参数
    """
    print("检查文件/etc/hosts.deny和/etc/hosts.allow中对终端登录限制的相关配置参数")
    files = ['/etc/hosts.deny', '/etc/hosts.allow']
    for file_path in files:
        # rules = []
        if os.path.exists(file_path):
            print(file_path + " 中规则如下")
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        print(line)
        else:
            print("不存在文件", file_path)
    print("--------------------------------")
    """
    应根据安全策略设置登录终端的操作超时锁定
    已在/etc/profile中为TMOUT设置了合理的操作超时时间
    """
    print("检查是否根据安全策略设置登录终端的操作超时锁定")
    tmout_value = None
    try:
        with open('/etc/profile', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('TMOUT='):
                    try:
                        tmout_value = int(line.split('=')[1])
                    except ValueError:
                        print("TMOUT 值不是一个有效的整数")
        if tmout_value is None:
            print("未在 /etc/profile 中找到 TMOUT 设置")
        else:
            if 600 <= tmout_value <= 3600:
                print("TMOUT设置为" + str(tmout_value), "，合理")
            else:
                print("TMOUT设置为" + str(tmout_value), "，不合理，应设置在 600 到 3600 秒之间")
    except FileNotFoundError:
        print("不存在 /etc/profile 文件")


def check_sudoers():
    """检查 sudoers 文件配置"""
    print("检查 sudoers 文件配置...")
    print(run_command("grep -E -v '^#|^$' /etc/sudoers"))


def check_ssh_config():
    """检查 SSH 配置"""
    print("检查 SSH 配置...")
    print(run_command("grep -E 'PermitRootLogin|PasswordAuthentication' /etc/ssh/sshd_config"))


def check_password_policy():
    """检查密码策略"""
    print("检查密码策略...")
    print(run_command("grep PASS_MAX_DAYS /etc/login.defs"))
    print(run_command("grep PASS_MIN_DAYS /etc/login.defs"))
    print(run_command("grep PASS_WARN_AGE /etc/login.defs"))


def check_firewall_status():
    """检查防火墙状态"""
    print("检查防火墙状态...")
    if run_command("command -v ufw"):
        print(run_command("ufw status"))
    elif run_command("command -v firewall-cmd"):
        print(run_command("firewall-cmd --state"))
    else:
        print("未检测到 ufw 或 firewalld")


def check_file_permissions():
    """检查重要文件权限"""
    print("检查重要文件权限...")
    print(run_command("ls -l /etc/passwd /etc/shadow /etc/gshadow /etc/group"))


def check_installed_packages():
    """检查已安装的软件包"""
    print("检查已安装的软件包...")
    if run_command("command -v dpkg"):
        print(run_command("dpkg -l"))
    elif run_command("command -v rpm"):
        print(run_command("rpm -qa"))
    else:
        print("未检测到 dpkg 或 rpm")


def check_running_services():
    """检查运行中的服务"""
    print("检查运行中的服务...")
    print(run_command("systemctl list-units --type=service --state=running"))


def check_kernel_params():
    """检查内核参数"""
    print("检查内核参数...")
    print(run_command("sysctl -a | grep -E 'net.ipv4.conf.all.accept_redirects|net.ipv4.conf.all.send_redirects'"))


def check_system_logs():
    """检查系统日志"""
    print("检查系统日志...")
    print(run_command("grep -i 'error\\|fail\\|critical' /var/log/syslog /var/log/messages /var/log/auth.log"))


def main():
    check_root()
    check_user_group_settings()
    check_view_control()
    check_security()
    check_source_control()

    # check_sudoers()
    # check_ssh_config()
    # check_password_policy()
    # check_firewall_status()
    # check_file_permissions()
    # check_installed_packages()
    # check_running_services()
    # check_kernel_params()
    # check_system_logs()
    print("基线扫描完成")


def schedule_check(func):
    # # 定时执行
    # schedule.every(1).hours.do(run_threaded, check_linux())
    # schedule.every(10).seconds.do(run_threaded, job2)
    # schedule.every(10).seconds.do(run_threaded, job3)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(5)
    schedule.every().days.do(func)


if __name__ == "__main__":
    main()
    # schedule_check(main())
