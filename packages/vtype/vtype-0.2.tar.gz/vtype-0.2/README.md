# 项目介绍

isinstance的升级版, 用于判断传入的第1个对象是否是后几个对象的实例.

# 作者资料

昵称: jutooy

邮箱: jutooy@qq.com

# 语法

    from vtype import vtype

    print( vtype('1', str, int, float) )
    # >>> True

    print( vtype(b'1', str, int, float) )
    # >>> False

    print( vtype(b'1', str, int, float, bytes) )
    # >>> True
