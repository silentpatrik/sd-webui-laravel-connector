import launch

if not launch.is_installed(" mysql.connector"):
    launch.run_pip("install mysql.connector")
