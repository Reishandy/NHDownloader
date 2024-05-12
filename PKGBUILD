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

  cd "$srcdir/$pkgname"
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  deactivate
}

package() {
  # Install the entire repository into /usr/share/NHDownloader
  install -dm755 "$pkgdir/usr/share/$pkgname"
  cp -a "$srcdir/$pkgname"/* "$pkgdir/usr/share/$pkgname"

  # Create a script that activates the virtual environment and runs NHDownloader.py
  echo '#!/bin/sh' > NHDownloader
  echo 'source /usr/share/NHDownloader/.venv/bin/activate' >> NHDownloader
  echo 'python /usr/share/NHDownloader/NHDownloader.py "$@"' >> NHDownloader

  # Make the script executable and install it into /usr/bin
  chmod +x NHDownloader
  install -Dm755 NHDownloader "$pkgdir/usr/bin/NHDownloader"
}