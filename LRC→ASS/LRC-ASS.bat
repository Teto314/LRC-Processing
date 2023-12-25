@echo off
chcp 65001 >nul 2>&1
setlocal

rem 获取当前脚本所在的目录
set "SCRIPT_DIR=%~dp0"

rem 要调用的 Python 脚本文件路径
set "PYTHON_SCRIPT1=D:\Enlarge\lrc-Code\LRC-Depart.py"
set "PYTHON_SCRIPT2=D:\Enlarge\lrc-Code\LRC-ASS.py"

rem 运行第一个 Python 脚本并传递当前目录作为参数
python "%PYTHON_SCRIPT1%" "%SCRIPT_DIR%"

rem 检查第一个脚本的执行结果
if errorlevel 1 (
    echo 第一个 Python 脚本执行失败，请检查日志或错误信息。
    goto :ERROR
)

echo.
echo ****************
echo * lrc 成功分割 *
echo ****************
echo.

rem 运行第二个 Python 脚本并传递当前目录作为参数
python "%PYTHON_SCRIPT2%" "%SCRIPT_DIR%"

rem 检查第二个脚本的执行结果
if errorlevel 1 (
    echo 第二个 Python 脚本执行失败，请检查日志或错误信息。
    goto :ERROR
)

echo.
echo ****************
echo * ass 成功生成 *
echo ****************
echo.

echo 按任意键退出...
pause >nul
goto :EOF

:ERROR
echo.
echo **************
echo * 发生错误 *
echo **************
echo.
echo 按任意键退出...
pause >nul

endlocal
