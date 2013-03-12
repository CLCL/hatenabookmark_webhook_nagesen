#!/usr/bin/perl
 
# throw.cgi ブックマークしたら投げ銭します。
# 説明：https://github.com/CLCL/hatenabookmark_webhook_nagesen
# 2009-06-07 ver 0.0.1 ファーストポスト
# 2009-10-03 ver 0.0.2 最新のMechでも動くように
# 2012-01-26 ver 0.0.3 はてなブログ対応
# 2013-02-26 ver 0.0.4 ポイント送信ページ変更に対応

 
use strict;
use warnings;
use CGI;
use Config::Pit;
use Encode;
use HTML::AccountAutoDiscovery;
use utf8;
use WWW::Mechanize;
 
# 初期設定
my $url_sendpoint = 'https://www.hatena.ne.jp/shop/point/sendpoint';
my $send_point = 10; # 送信するポイント（はてな手数料別）
my $login;
my $config = pit_get('hatena.ne.jp');
die "not preset account data in Pit." if !%$config;
my $my_id    = $config->{id      } or die 'id not found.';
my $password = $config->{password} or die 'password not found.';
my $auth_key = $config->{auth_key} or die 'auth_key not found.';
 
my $q = CGI->new;
my $mech = WWW::Mechanize->new;
$mech->agent_alias('Windows IE 6');
 
{ # メインルーチン
  # 認証
  if ( $q->param('key') ne $auth_key ) {
      die "Authentication failed";
  }
  # メソッド確認
  if ( $q->param('status') eq 'add' ) {
    # エントリーの情報
    my $req = $q->Vars();
    nagesen( $req );
  }
  # はてなブックマークWeb Hook用リザルト
  print $q->header('text/plain');
  print 'ok';
}
exit;
 
sub nagesen {
  my $req = shift;
  my $url = $req->{url};
  my @account = HTML::AccountAutoDiscovery->find( $url );
  unless( @account ) { @account = find_hatenablog( $url ); }
  sub find_hatenablog {
    my $url = shift;
    use LWP::Simple;
    my @r;
    my $c = get( $url );
    $c =~ s/.+(<html.+?>).+/$1/so;
    if ( $c =~ m{data-admin-domain="http://blog.hatena.ne.jp"} ) {
      if ( $c =~ m{data-author="(.+)"} ) {
        push @r,{account => $1, service => 'http://blog.hatena.ne.jp' };
      }
    }
    return  @r;
  }
  
  foreach my $item ( @account ) {
    my $send_id = $item->{account}; # account name
    send_hatenapoint( $req, $send_id );
    last; # HTMLに複数のIDを埋め込んでいた場合最初の人の分
          # だけ対応（同じ人がID埋め込みまくるとポイント
          # 送信しまくるのを防ぐ）
  }
  return;
}
 
sub login_hatenapoint {
# はてなにログインします
  $mech->get( $url_sendpoint );
  # ログインを促す画面に遷移済
  $mech->follow_link( text => mech_encode('ログイン') );
  # ログイン画面に遷移済
  $mech->set_visible( $my_id, $password );
  $mech->submit();
  # ログイン済み画面に遷移済
  $mech->follow_link( text => mech_encode('こちら') );
  # 投げ銭画面に遷移済
  $login = 1;
  return;
}
 
sub send_hatenapoint {
# はてなポイント送信をします
  my $req     = shift;
  my $send_id = shift;
  unless ( $login ) {
    login_hatenapoint();
  }
  # ログイン済みの状態
  $mech->get( $url_sendpoint );
  # はてなポイント送信のページに遷移済
  # ポイント送信メッセージ組み立て
  my $send_message = decode('utf8', $req->{title})
    ."($req->{url}) をブックマークしました。投げ銭いたします。"
    .'投げ銭スクリプト：http://svn.coderepos.org/share/lang/'
    .'perl/misc/hatenabookmark_webhook_nagesen/';
  # ポイント送信用パラメータ入力
  $mech->set_visible(
    $send_id, $send_point, # 2013年変更で匿名送信はなくなりました
    mech_encode( $send_message )
  );
  $mech->submit();
  # confirm画面に遷移済
  my $confirm_str = mech_encode('パスワードを入力してください');
  return unless ( $mech->content() =~ m/$confirm_str/); # 送信確認ページ?
  $mech->set_visible( $password); # 2013年変更でconfirmでパスワード入力となった
  $mech->click_button( value => mech_encode('送信する') );
  #open my $fh, '>', 'log.html';
  #print $fh $mech->content();
  #close $fh;
  return;
}
 
sub mech_encode {
# WWW::Mechanize 1.21_01以降の挙動に対応
  my $str = shift;
  if ( ( $WWW::Mechanize::VERSION ) < 1.21 ) {
    $str = encode( 'utf8', $str );
  }
  return $str;
}
 
__END__
