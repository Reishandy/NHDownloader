pkgname=NHDownloader
pkgver=1.0
pkgrel=1
pkgdesc="A Python-based command-line tool that allows you to download doujin from nhentai.net"
arch=('any')
url="https://github.com/Reishandy/NHDownloader"
license=('MIT')
depends=('python' 'python-pip')

build() {
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  deactivate
}

package() {
  install -Dm755 NHDownloader.py "$pkgdir/usr/bin/NHDownloader"
}