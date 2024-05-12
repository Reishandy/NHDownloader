pkgname=NHDownloader
pkgver=1.0
pkgrel=1
pkgdesc="A Python-based command-line tool that allows you to download doujin from nhentai.net"
arch=('any')
url="https://github.com/Reishandy/NHDownloader"
license=('MIT')
depends=('python')
makedepends=('git' 'python-pip')

build() {
  # Clone the repository into the src directory
  git clone https://github.com/Reishandy/NHDownloader.git "$srcdir/$pkgname"
}

package() {
  # Install the entire repository into /usr/share/NHDownloader
  install -dm755 "$pkgdir/usr/share/$pkgname"
  cp -a "$srcdir/$pkgname"/* "$pkgdir/usr/share/$pkgname"

  cd "$pkgdir/usr/share/$pkgname"
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  deactivate

  # Create a script that runs NHDownloader.py with the Python interpreter in the virtual environment
  echo '#!/bin/sh' > /tmp/NHDownloader
  echo '/usr/share/NHDownloader/.venv/bin/python /usr/share/NHDownloader/NHDownloader.py "$@"' >> /tmp/NHDownloader

  # Make the script executable and install it into /usr/bin
  chmod +x /tmp/NHDownloader
  install -Dm755 /tmp/NHDownloader "$pkgdir/usr/bin/NHDownloader"
}