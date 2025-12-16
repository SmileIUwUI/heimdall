import click

from heimdall import __version__
from heimdall.core import Controller


def show_banner():
    """Display Heimdall ASCII banner"""
    banner = f"""
  _    _ ______ _____ __  __ _____          _      _      
 | |  | |  ____|_   _|  \/  |  __ \   /\   | |    | |     
 | |__| | |__    | | | \  / | |  | | /  \  | |    | |     
 |  __  |  __|   | | | |\/| | |  | |/ /\ \ | |    | |     
 | |  | | |____ _| |_| |  | | |__| / ____ \| |____| |____ 
 |_|  |_|______|_____|_|  |_|_____/_/    \_\______|______|
                                                          
    Tor Network Search Tool • {__version__}
    """
    click.echo(click.style(banner, fg='cyan', bold=True))

def show_disclaimer():
    disclaimer = """
################################################################
                    IMPORTANT NOTICE
################################################################

Heimdall accesses the Tor network, which contains:
• Legitimate privacy-focused services
• Potentially illegal content
• Unverified and risky websites

LEGAL WARNING:
- Accessing certain content may be illegal in your jurisdiction
- This tool does NOT provide anonymity by itself
- Your ISP can detect Tor usage
- Law enforcement may monitor Tor exit nodes

ETHICAL USE:
✓ Use for academic research
✓ Use to access legitimate .onion services

PROHIBITED USE:
✗ Illegal activities
✗ Unauthorized access
✗ Harassment or abuse
✗ Distribution of malicious content

By continuing, you confirm that:
1. You understand these risks
2. You use this tool responsibly
3. You comply with applicable laws

################################################################"""
    click.echo(click.style(disclaimer, fg='red', bold=True))

@click.group()
def app():
    click.clear()
    show_banner()
    show_disclaimer()

@app.command()
def search():
    controller = Controller()