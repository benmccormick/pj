# pj formula, based on fpp's formula https://github.com/facebook/PathPicker/blob/master/fpp.rb

class Pj < Formula
  desc "Projects for the command line inspired by Sublime Text"
  homepage "https://benmccormick.github.io/pj/"
  url "https://github.com/benmccormick/pj/archive/0.0.1.tar.gz"
  version "0.0.1"
  sha256 "7272ee5e29dfd07485524f4726f9adc6deb77ea793843bc0bb7e58ee2d9cd64f"

  depends_on :python if MacOS.version <= :snow_leopard

  def install
    # we need to copy the bash file and source python files
    libexec.install Dir["*"]
    # and then symlink the bash file
    bin.install_symlink libexec/"pj"
  end

  test do
    system bin/"pj", "--help"
  end
end
