from rich.console import Console

console = Console()

console.warn = lambda *args: console.log(*args)
console.error = lambda *args: console.log(*args)
console.debug = lambda *args: None  # console.log(*args)
