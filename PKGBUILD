pkgname=NHDownloader
pkgver=1.0
pkgrel=1
pkgdesc="A Python-based command-line tool that allows you to download doujin from nhentai.net"
arch=('any')
url="https://github.com/Reishandy/NHDownloader"
license=('MIT')
depends=('python' 'python-pip')
source=("$pkgname-$pkgver.tar.gz::https://github.com/Reishandy/NHDownloader/archive/refs/tags/v$pkgver.tar.gz"
        "requirements.txt::https://raw.githubusercontent.com/Reishandy/NHDownloader/v$pkgver/requirements.txt")
sha256sums=('SKIP' 'SKIP')

build() {
  cd "$pkgname-$pkgver"
  python -m venv .venv
  source .venv/bin/activate
  pip install -r ../requirements.txt
  deactivate
}

package() {
  cd "$pkgname-$pkgver"
  install -Dm755 NHDownloader.py "$pkgdir/usr/bin/NHDownloader"
}