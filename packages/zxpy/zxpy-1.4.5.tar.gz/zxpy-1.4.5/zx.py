"""
zxpy: Shell scripts made simple

To run script(s):

    zxpy script.py

To start a REPL:

    zxpy

If you haven't installed zxpy globally, you can run it by doing:

    path/to/python -m zx [...]

zxpy files can also be executed directly on a POSIX system by adding
the shebang:

    #! /use/bin/env zxpy

...to the top of your file, and executing it directly like a shell
script. Note that this requires you to have zxpy installed globally.
"""
import ast
import code
import inspect
import subprocess
import shlex
import sys
import traceback
from typing import Literal, Optional, Tuple, Union, overload


def cli() -> None:
    """
    Simple CLI interface.

    To run script(s):

        zxpy script.py

    To start a REPL:

        zxpy
    """
    # Remove zxpy executable from argv
    sys.argv = sys.argv[1:]

    if len(sys.argv) == 0:
        setup_zxpy_repl()
        return

    filename = sys.argv[0]
    with open(filename) as file:
        module = ast.parse(file.read())
        run_zxpy(filename, module)


@overload
def run_shell(command: str) -> str: ...
@overload
def run_shell(command: str, print_it: Literal[False]) -> str: ...
@overload
def run_shell(command: str, print_it: Literal[True]) -> None: ...


def run_shell(command: str, print_it: bool = False) -> Optional[str]:
    """This is indirectly run when doing ~'...'"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    )
    assert process.stdout is not None

    if not print_it:
        return process.stdout.read().decode()

    while True:
        char = process.stdout.read(1)
        if not char:
            break

        sys.stdout.buffer.write(char)
        sys.stdout.flush()

    return None


def shlex_quote(string: str) -> str:
    """Simple wrapper for shlex.quote"""
    return shlex.quote(string)


def run_shell_alternate(command: str) -> Tuple[str, str, int]:
    """Like run_shell but returns 3 values: stdout, stderr and return code"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    process.wait()
    assert process.stdout is not None
    assert process.stderr is not None
    assert process.returncode is not None

    return (
        process.stdout.read().decode(),
        process.stderr.read().decode(),
        process.returncode,
    )


def run_zxpy(filename: str, module: ast.Module) -> None:
    """Runs zxpy on a given file"""
    patch_shell_commands(module)
    code = compile(module, filename, mode='exec')
    exec(
        code,
        {
            '__name__': '__main__',
            'run_shell': run_shell,
            'run_shell_alternate': run_shell_alternate,
            'shlex_quote': shlex_quote,
        },
    )


def patch_shell_commands(module: Union[ast.Module, ast.Interactive]) -> None:
    """Patches the ast module to add zxpy functionality"""
    shell_runner = ShellRunner()
    shell_runner.visit(module)

    ast.fix_missing_locations(module)


def quote_fstring_args(fstring: ast.JoinedStr) -> None:
    for index, node in enumerate(fstring.values):
        if isinstance(node, ast.FormattedValue):
            # If it's marked as a raw shell string, then don't escape
            if (
                isinstance(node.format_spec, ast.JoinedStr)
                and len(node.format_spec.values) == 1
                and node.format_spec.values[0].value == 'raw'
            ):
                node.format_spec = None
                continue

            fstring.values[index] = ast.Call(
                func=ast.Name(id='shlex_quote', ctx=ast.Load()),
                args=[node],
                keywords=[],
            )


class ShellRunner(ast.NodeTransformer):
    """Replaces the ~'...' syntax with run_shell(...)"""
    @staticmethod
    def modify_expr(
            expr: ast.expr,
            return_stderr_and_returncode: bool = False,
            print_it: bool = False,
    ) -> ast.expr:
        if (
            isinstance(expr, ast.UnaryOp)
            and isinstance(expr.op, ast.Invert)
            and isinstance(expr.operand, (ast.Str, ast.JoinedStr))
        ):
            if isinstance(expr.operand, ast.JoinedStr):
                quote_fstring_args(expr.operand)

            function_name = (
                'run_shell_alternate'
                if return_stderr_and_returncode
                else 'run_shell'
            )

            if print_it:
                keywords = [
                    ast.keyword(
                        arg='print_it',
                        value=ast.Constant(value=True),
                    )
                ]
            else:
                keywords = []

            return ast.Call(
                func=ast.Name(id=function_name, ctx=ast.Load()),
                args=[expr.operand],
                keywords=keywords,
            )

        return expr

    def visit_Expr(self, expr: ast.Expr) -> ast.Expr:
        expr.value = self.modify_expr(expr.value, print_it=True)
        super().generic_visit(expr)
        return expr

    def visit_Assign(self, assign: ast.Assign) -> ast.Assign:
        assign.value = self.modify_expr(
            assign.value,
            return_stderr_and_returncode=isinstance(assign.targets[0], ast.Tuple),
        )

        super().generic_visit(assign)
        return assign

    def visit_Call(self, call: ast.Call) -> ast.Call:
        for index, arg in enumerate(call.args):
            call.args[index] = self.modify_expr(arg)

        super().generic_visit(call)
        return call

    def visit_Attribute(self, attr: ast.Attribute) -> ast.Attribute:
        attr.value = self.modify_expr(attr.value)
        super().generic_visit(attr)
        return attr


def setup_zxpy_repl() -> None:
    """Sets up a zxpy interactive session"""
    print("zxpy shell")
    print("Python", sys.version)
    print()

    install()


def install() -> None:
    """
    Starts an interactive shell that looks like the REPL, but with zxpy features.

    Useful for setting up a zxpy session in an already running REPL.
    Simply do:

        >>> import zx; zx.install()

    and zxpy should be enabled in the REPL.
    """
    # Get locals from parent frame
    frames = inspect.getouterframes(inspect.currentframe())
    if len(frames) > 1:
        parent_frame = frames[1]
        parent_locals = parent_frame.frame.f_locals
        locals().update(parent_locals)

    # For tab completion and arrow key support
    if sys.platform != 'win32':
        import readline
        readline.parse_and_bind("tab: complete")

    command = ''
    continued_command = False
    while True:
        try:
            prompt = '... ' if continued_command else '>>> '
            new_input = input(prompt)
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            print()
            sys.exit(0)

        # TODO: refactor the next 10 lines.
        # probably move command = '...' stuff somewhere else
        if continued_command:
            command += '\n'
        else:
            command = ''

        if new_input != '':
            command += new_input
        else:
            continued_command = False

        if continued_command:
            continue

        try:
            ast_obj = ast.parse(command, '<input>', 'single')
        except SyntaxError:
            try:
                code_obj = code.compile_command(command)
                if code_obj is None:
                    continued_command = True
                    continue

            except BaseException:
                traceback.print_exc()
                continue

        assert isinstance(ast_obj, ast.Interactive)
        patch_shell_commands(ast_obj)

        try:
            code_obj = compile(ast_obj, '<input>', 'single')
            assert code_obj is not None
            exec(code_obj)

        except SystemExit as e:
            sys.exit(e.code)

        except BaseException:
            traceback.print_exc()


if __name__ == '__main__':
    cli()
