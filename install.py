import launch

if not launch.is_installed("mysql-connector-python"):
    launch.run_pip("install mysql-connector-python")
