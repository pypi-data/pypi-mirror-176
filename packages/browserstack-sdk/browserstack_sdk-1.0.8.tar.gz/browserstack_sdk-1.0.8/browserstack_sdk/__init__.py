# coding: UTF-8
import sys
bstack1ll1_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1l1l_opy_ = 7
def bstack1ll_opy_ (bstack1_opy_):
    global bstack1l_opy_
    bstack1l11_opy_ = ord (bstack1_opy_ [-1])
    bstack1l1_opy_ = bstack1_opy_ [:-1]
    bstackl_opy_ = bstack1l11_opy_ % len (bstack1l1_opy_)
    bstack111_opy_ = bstack1l1_opy_ [:bstackl_opy_] + bstack1l1_opy_ [bstackl_opy_:]
    if bstack1ll1_opy_:
        bstack11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack11_opy_ + bstack1l11_opy_) % bstack1l1l_opy_) for bstack11_opy_, char in enumerate (bstack111_opy_)])
    else:
        bstack11l_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack11_opy_ + bstack1l11_opy_) % bstack1l1l_opy_) for bstack11_opy_, char in enumerate (bstack111_opy_)])
    return eval (bstack11l_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
from packaging import version
from browserstack.local import Local
bstack11l1l_opy_ = {
	bstack1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢌ"): bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩࢍ"),
  bstack1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩࢎ"): bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪ࢏"),
  bstack1ll_opy_ (u"ࠨࡱࡶࠫ࢐"): bstack1ll_opy_ (u"ࠩࡲࡷࠬ࢑"),
  bstack1ll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࢒"): bstack1ll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ࢓"),
  bstack1ll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ࢔"): bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭࢕"),
  bstack1ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ࢖"): bstack1ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࠩࢗ"),
  bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ࢘"): bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥ࢙ࠩ"),
  bstack1ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦ࢚ࠩ"): bstack1ll_opy_ (u"ࠬࡴࡡ࡮ࡧ࢛ࠪ"),
  bstack1ll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬ࢜"): bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫ࠬ࢝"),
  bstack1ll_opy_ (u"ࠨࡥࡲࡲࡸࡵ࡬ࡦࡎࡲ࡫ࡸ࠭࢞"): bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡲࡸࡵ࡬ࡦࠩ࢟"),
  bstack1ll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࢠ"): bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࢡ"),
  bstack1ll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩࢢ"): bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩࢣ"),
  bstack1ll_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࠭ࢤ"): bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡷ࡫ࡧࡩࡴ࠭ࢥ"),
  bstack1ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨࢦ"): bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨࢧ"),
  bstack1ll_opy_ (u"ࠫࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫࢨ"): bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫࢩ"),
  bstack1ll_opy_ (u"࠭ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫࢪ"): bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫࢫ"),
  bstack1ll_opy_ (u"ࠨࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪࢬ"): bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪࢭ"),
  bstack1ll_opy_ (u"ࠪࡶࡪࡹ࡯࡭ࡷࡷ࡭ࡴࡴࠧࢮ"): bstack1ll_opy_ (u"ࠫࡷ࡫ࡳࡰ࡮ࡸࡸ࡮ࡵ࡮ࠨࢯ"),
  bstack1ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧࢰ"): bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨࢱ"),
  bstack1ll_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭ࢲ"): bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭ࢳ"),
  bstack1ll_opy_ (u"ࠩ࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧࢴ"): bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧࢵ"),
  bstack1ll_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫࢶ"): bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫࢷ"),
  bstack1ll_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡳࠨࢸ"): bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦࡰࡧࡏࡪࡿࡳࠨࢹ"),
  bstack1ll_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪࢺ"): bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡸࡸࡴ࡝ࡡࡪࡶࠪࢻ"),
  bstack1ll_opy_ (u"ࠪ࡬ࡴࡹࡴࡴࠩࢼ"): bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡬ࡴࡹࡴࡴࠩࢽ"),
  bstack1ll_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭ࢾ"): bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡦࡤࡣࡦ࡬ࡪ࠭ࢿ"),
  bstack1ll_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨࣀ"): bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨࣁ"),
  bstack1ll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬࣂ"): bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬࣃ"),
  bstack1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࣄ"): bstack1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬࣅ"),
  bstack1ll_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࣆ"): bstack1ll_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬࣇ"),
  bstack1ll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨࣈ"): bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩࣉ"),
  bstack1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧ࣊"): bstack1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨ࣋"),
  bstack1ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬ࣌"): bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬ࣍"),
  bstack1ll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨ࣎"): bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨ࣏"),
  bstack1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨ࣐"): bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶ࣑ࠫ"),
  bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࣒࠭"): bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࣓࠭"),
  bstack1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ࣔ"): bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡰࡷࡵࡧࡪ࠭ࣕ"),
}
bstack1l111_opy_ = [
  bstack1ll_opy_ (u"ࠨࡱࡶࠫࣖ"),
  bstack1ll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࣗ"),
  bstack1ll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬࣘ"),
  bstack1ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࣙ"),
  bstack1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩࣚ"),
  bstack1ll_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࣛ"),
  bstack1ll_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧࣜ"),
]
bstack1l1l1_opy_ = {
  bstack1ll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࣝ"): bstack1ll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࣞ"),
  bstack1ll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬࣟ"): [bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࣠"), bstack1ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ࣡")],
  bstack1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ࣢"): bstack1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࣣࠬ"),
  bstack1ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬࣤ"): bstack1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩࣥ"),
  bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣦ"): [bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬࣧ"), bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫࣨ")],
  bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࣩࠧ"): bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࣪"),
  bstack1ll_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬ࣫"): bstack1ll_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧ࣬"),
  bstack1ll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰ࣭ࠪ"): [bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱ࣮ࠫ"), bstack1ll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࣯࠭")],
  bstack1ll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࣰࠬ"): [bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨࣱ"), bstack1ll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࠨࣲ")]
}
bstack11ll_opy_ = {
  bstack1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨࣳ"): [bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫࣴ"), bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫࣵ")]
}
bstack1ll11_opy_ = [
  bstack1ll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࣶࠫ"),
  bstack1ll_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩࣷ"),
  bstack1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ࣸ"),
  bstack1ll_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨࣹ"),
  bstack1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࣺࠫ"),
  bstack1ll_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨࣻ"),
  bstack1ll_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧࣼ")
]
bstack1llll_opy_ = [
  bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࣽ"),
  bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࣾ"),
  bstack1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣿ"),
  bstack1ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨऀ"),
  bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ"),
  bstack1ll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬं"),
  bstack1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧः"),
  bstack1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩऄ"),
  bstack1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩअ"),
]
bstack1111_opy_ = [
  bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ"),
  bstack1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧइ"),
]
bstack1l11l_opy_ = bstack1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡻࡩ࠵ࡨࡶࡤࠪई")
bstack1l1ll_opy_ = bstack1ll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧ࠭उ")
bstack1lll1_opy_ = {
  bstack1ll_opy_ (u"ࠫࡨࡸࡩࡵ࡫ࡦࡥࡱ࠭ऊ"): 50,
  bstack1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫऋ"): 40,
  bstack1ll_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧऌ"): 30,
  bstack1ll_opy_ (u"ࠧࡪࡰࡩࡳࠬऍ"): 20,
  bstack1ll_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧऎ"): 10
}
DEFAULT_LOG_LEVEL = bstack1lll1_opy_[bstack1ll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧए")]
bstack111l_opy_ = bstack1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩऐ")
bstack11lll_opy_ = bstack1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩऑ")
bstack11l1_opy_ = bstack1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪऒ")
bstack11ll1_opy_ = [bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧओ"), bstack1ll_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧऔ")]
bstack1ll1l_opy_ = [bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫक"), bstack1ll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫख")]
bstack1111ll1_opy_ = bstack1ll_opy_ (u"ࠪࡗࡪࡺࡴࡪࡰࡪࠤࡺࡶࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠯ࠤࡺࡹࡩ࡯ࡩࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡀࠠࡼࡿࠪग")
bstack1lll1l_opy_ = bstack1ll_opy_ (u"ࠫࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡴࡧࡷࡹࡵࠧࠧघ")
bstack1ll1ll_opy_ = bstack1ll_opy_ (u"ࠬࡖࡡࡳࡵࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧङ")
bstack1l1lll_opy_ = bstack1ll_opy_ (u"࠭ࡕࡴ࡫ࡱ࡫ࠥ࡮ࡵࡣࠢࡸࡶࡱࡀࠠࡼࡿࠪच")
bstack11l1l1l_opy_ = bstack1ll_opy_ (u"ࠧࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࢀࢃࠧछ")
bstack1lll11l_opy_ = bstack1ll_opy_ (u"ࠨࡔࡨࡧࡪ࡯ࡶࡦࡦࠣ࡭ࡳࡺࡥࡳࡴࡸࡴࡹ࠲ࠠࡦࡺ࡬ࡸ࡮ࡴࡧࠨज")
bstack111lll_opy_ = bstack1ll_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡦࠧझ")
bstack111l11_opy_ = bstack1ll_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡷࡵࡢࡰࡶࠣࡥࡳࡪࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࡮࡬ࡦࡷࡧࡲࡺࠢࡳࡥࡨࡱࡡࡨࡧࡶࠤࡹࡵࠠࡳࡷࡱࠤࡷࡵࡢࡰࡶࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡵࡳࡧࡵࡴࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡲࡩࡣࡴࡤࡶࡾࡦࠧञ")
bstack11ll1l1_opy_ = bstack1ll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡸ࡯ࡣࡱࡷ࠰ࠥࡶࡡࡣࡱࡷࠤࡦࡴࡤࠡࡵࡨࡰࡪࡴࡩࡶ࡯࡯࡭ࡧࡸࡡࡳࡻࠣࡴࡦࡩ࡫ࡢࡩࡨࡷࠥࡺ࡯ࠡࡴࡸࡲࠥࡸ࡯ࡣࡱࡷࠤࡹ࡫ࡳࡵࡵࠣ࡭ࡳࠦࡰࡢࡴࡤࡰࡱ࡫࡬࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡵࡳࡧࡵࡴࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠰ࡴࡦࡨ࡯ࡵࠢࡵࡳࡧࡵࡴࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࡱ࡯ࡢࡳࡣࡵࡽࡥ࠭ट")
bstack11lllll_opy_ = bstack1ll_opy_ (u"ࠬࡎࡡ࡯ࡦ࡯࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥ࡯ࡳࡸ࡫ࠧठ")
bstack11ll11_opy_ = bstack1ll_opy_ (u"࠭ࡁ࡭࡮ࠣࡨࡴࡴࡥࠢࠩड")
bstack1l11l1l_opy_ = bstack1ll_opy_ (u"ࠧࡄࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࠦࡡࡵࠢࠥࡿࢂࠨ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡧࡱࡻࡤࡦࠢࡤࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡧ࡫࡯ࡩࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯ࡧࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡺࡥࡴࡶࡶ࠲ࠬढ")
bstack1ll111l_opy_ = bstack1ll_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡴࡨࡨࡪࡴࡴࡪࡣ࡯ࡷࠥࡴ࡯ࡵࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡷ࡬ࡪࡳࠠࡪࡰࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠤࡦࡹࠠࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥࠤࡦࡴࡤࠡࠤࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠧࠦ࡯ࡳࠢࡶࡩࡹࠦࡴࡩࡧࡰࠤࡦࡹࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳ࠻ࠢࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦࠥࡧ࡮ࡥࠢࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞ࠨࠧण")
bstack111lll1_opy_ = bstack1ll_opy_ (u"ࠩࡐࡥࡱ࡬࡯ࡳ࡯ࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠦࢀࢃࠢࠨत")
bstack1lllll1l_opy_ = bstack1ll_opy_ (u"ࠪࡉࡳࡩ࡯ࡶࡰࡷࡩࡷ࡫ࡤࠡࡧࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣ࠱ࠥࢁࡽࠨथ")
bstack1lll1lll_opy_ = bstack1ll_opy_ (u"ࠫࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠫद")
bstack111l1l1_opy_ = bstack1ll_opy_ (u"࡙ࠬࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰࠬध")
bstack1l1l1ll_opy_ = bstack1ll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠤ࡮ࡹࠠ࡯ࡱࡺࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠦ࠭न")
bstack1lll11l1_opy_ = bstack1ll_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲ࠺ࠡࡽࢀࠫऩ")
bstack1l1l1l1_opy_ = bstack1ll_opy_ (u"ࠨࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡥ࡭ࡳࡧࡲࡺࠢࡺ࡭ࡹ࡮ࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࡾࢁࠬप")
bstack1ll11l_opy_ = bstack1ll_opy_ (u"ࠩࡘࡴࡩࡧࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠪफ")
bstack1l11ll1_opy_ = bstack1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠩब")
bstack1ll1111l_opy_ = bstack1ll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࠥࡧ࡮ࠡࡣࡳࡴࡷࡵࡰࡳ࡫ࡤࡸࡪࠦࡆࡘࠢࠫࡶࡴࡨ࡯ࡵ࠱ࡳࡥࡧࡵࡴࠪࠢ࡬ࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠯ࠤࡸࡱࡩࡱࠢࡷ࡬ࡪࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡮ࡩࡾࠦࡩ࡯ࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡪࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡳࡪ࡯ࡳࡰࡪࠦࡰࡺࡶ࡫ࡳࡳࠦࡳࡤࡴ࡬ࡴࡹࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡢࡰࡼࠤࡋ࡝࠮ࠨभ")
bstack11111_opy_ = bstack1ll_opy_ (u"࡙ࠬࡥࡵࡶ࡬ࡲ࡬ࠦࡨࡵࡶࡳࡔࡷࡵࡸࡺ࠱࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾࠦࡩࡴࠢࡱࡳࡹࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡲࡲࠥࡩࡵࡳࡴࡨࡲࡹࡲࡹࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡵࡦࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࠬࢀࢃࠩ࠭ࠢࡳࡰࡪࡧࡳࡦࠢࡸࡴ࡬ࡸࡡࡥࡧࠣࡸࡴࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭࠿࠿࠷࠲࠵࠴࠰ࠡࡱࡵࠤࡷ࡫ࡦࡦࡴࠣࡸࡴࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡥࡱࡦࡷ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠱ࡵࡹࡳ࠳ࡴࡦࡵࡷࡷ࠲ࡨࡥࡩ࡫ࡱࡨ࠲ࡶࡲࡰࡺࡼࠧࡵࡿࡴࡩࡱࡱࠤ࡫ࡵࡲࠡࡣࠣࡻࡴࡸ࡫ࡢࡴࡲࡹࡳࡪ࠮ࠨम")
bstack11l111_opy_ = bstack1ll_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲࠳࠭य")
bstack1l1l111_opy_ = bstack1ll_opy_ (u"ࠧࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡧࡦࡰࡨࡶࡦࡺࡥࡥࠢࡷ࡬ࡪࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠥࠬर")
bstack1l1lllll_opy_ = bstack1ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫࠮ࠡࡽࢀࠫऱ")
bstack1l1l11l_opy_ = bstack1ll_opy_ (u"ࠩࡈࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡺࠠ࡭ࡧࡤࡷࡹࠦ࠱ࠡ࡫ࡱࡴࡺࡺࠬࠡࡴࡨࡧࡪ࡯ࡶࡦࡦࠣ࠴ࠬल")
from ._version import __version__
bstack1lll1111_opy_ = None
CONFIG = {}
bstack11ll111_opy_ = None
bstack11111l_opy_ = None
bstack1ll1lll1_opy_ = None
bstack11l1l11_opy_ = -1
bstack1llll1_opy_ = DEFAULT_LOG_LEVEL
bstack1l1lll1_opy_ = 1
bstack1lllll1_opy_ = False
bstack11llll_opy_ = bstack1ll_opy_ (u"ࠪࠫळ")
bstack11llll1_opy_ = bstack1ll_opy_ (u"ࠫࠬऴ")
bstack11l11l1_opy_ = None
bstack1llllll_opy_ = None
bstack111ll_opy_ = None
bstack11l11l_opy_ = None
bstack1l1l1l_opy_ = None
bstack111l111_opy_ = None
bstack1111111_opy_ = None
bstack1ll11l1l_opy_ = None
bstack1l1ll11_opy_ = None
logger = logging.getLogger(__name__)
def bstack1lllll11_opy_():
  global CONFIG
  global bstack1llll1_opy_
  if bstack1ll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧव") in CONFIG:
    bstack1llll1_opy_ = bstack1lll1_opy_[CONFIG[bstack1ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨश")]]
  logging.basicConfig(level=bstack1llll1_opy_,
                      format=bstack1ll_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬष"),
                      datefmt=bstack1ll_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪस"))
def bstack1ll111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11111ll_opy_():
  bstack1ll1l1_opy_ = bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬह")
  bstack1ll11lll_opy_ = os.path.abspath(bstack1ll1l1_opy_)
  if not os.path.exists(bstack1ll11lll_opy_):
    bstack1ll1l1_opy_ = bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧऺ")
    bstack1ll11lll_opy_ = os.path.abspath(bstack1ll1l1_opy_)
    if not os.path.exists(bstack1ll11lll_opy_):
      bstack1l11111_opy_(
        bstack1l11l1l_opy_.format(os.getcwd()))
  with open(bstack1ll11lll_opy_, bstack1ll_opy_ (u"ࠫࡷ࠭ऻ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1l11111_opy_(bstack111lll1_opy_.format(str(exc)))
def bstack1ll1l1l_opy_(config):
  bstack1lll1ll_opy_ = config.keys()
  bstack11ll1l_opy_ = []
  if bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ़") in config:
    bstack11ll1l_opy_ = config[bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩऽ")]
  for bstack1111l1l_opy_, bstack1ll1llll_opy_ in bstack11l1l_opy_.items():
    if bstack1ll1llll_opy_ in bstack1lll1ll_opy_:
      config[bstack1111l1l_opy_] = config[bstack1ll1llll_opy_]
      del config[bstack1ll1llll_opy_]
  for bstack1111l1l_opy_, bstack1ll1llll_opy_ in bstack1l1l1_opy_.items():
    for platform in bstack11ll1l_opy_:
      if isinstance(bstack1ll1llll_opy_, list):
        for bstack1l1ll1l_opy_ in bstack1ll1llll_opy_:
          if bstack1l1ll1l_opy_ in platform:
            platform[bstack1111l1l_opy_] = platform[bstack1l1ll1l_opy_]
            del platform[bstack1l1ll1l_opy_]
            break
      elif bstack1ll1llll_opy_ in platform:
        platform[bstack1111l1l_opy_] = platform[bstack1ll1llll_opy_]
        del platform[bstack1ll1llll_opy_]
  for bstack1111l1l_opy_, bstack1ll1llll_opy_ in bstack11ll_opy_.items():
    for bstack1l1ll1l_opy_ in bstack1ll1llll_opy_:
      if bstack1l1ll1l_opy_ in bstack1lll1ll_opy_:
        config[bstack1111l1l_opy_] = config[bstack1l1ll1l_opy_]
        del config[bstack1l1ll1l_opy_]
  for bstack1l1ll1l_opy_ in list(config):
    for bstack11l1ll1_opy_ in bstack1111_opy_:
      if bstack1l1ll1l_opy_.lower() == bstack11l1ll1_opy_.lower() and bstack1l1ll1l_opy_ != bstack11l1ll1_opy_:
        config[bstack11l1ll1_opy_] = config[bstack1l1ll1l_opy_]
        del config[bstack1l1ll1l_opy_]
  return config
def bstack1lll111_opy_(config):
  global bstack11llll1_opy_
  if bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫा") in config and str(config[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬि")]).lower() != bstack1ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨी"):
    if not bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧु") in config:
      config[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨू")] = {}
    if not bstack1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ") in config[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॄ")]:
      if bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩॅ") in os.environ:
        config[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॆ")][bstack1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫे")] = os.environ[bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬै")]
      else:
        current_time = datetime.datetime.now()
        bstack1lllllll_opy_ = current_time.strftime(bstack1ll_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨॉ"))
        hostname = socket.gethostname()
        bstack1llll11l_opy_ = bstack1ll_opy_ (u"ࠬ࠭ॊ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
        identifier = bstack1ll_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨो").format(bstack1lllllll_opy_, hostname, bstack1llll11l_opy_)
        config[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫौ")][bstack1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ्ࠪ")] = identifier
    bstack11llll1_opy_ = config[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ॎ")][bstack1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬॏ")]
  return config
def bstack11l1l1_opy_(config):
  if bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧॐ") in config and config[bstack1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ॑")] not in bstack1ll1l_opy_:
    return config[bstack1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺ॒ࠩ")]
  elif bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓") in os.environ:
    return os.environ[bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ॔")]
  else:
    return None
def bstack1lll1l1l_opy_(config):
  if bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬॕ") in config:
    return config[bstack1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ॖ")]
  elif bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠧॗ") in os.environ:
    return os.environ[bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨक़")]
  else:
    return None
def bstack111l1l_opy_(config):
  if bstack1ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨख़") in config and config[bstack1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩग़")] not in bstack11ll1_opy_:
    return config[bstack1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪज़")]
  elif bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪड़") in os.environ:
    return os.environ[bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫढ़")]
  else:
    return None
def bstack1l11lll_opy_(config):
  if not bstack111l1l_opy_(config) or not bstack11l1l1_opy_(config):
    return True
  else:
    return False
def bstack1ll11l1_opy_(config):
  if bstack1ll111_opy_() < version.parse(bstack1ll_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪफ़")):
    return False
  if bstack1ll111_opy_() >= version.parse(bstack1ll_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫय़")):
    return True
  if bstack1ll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ॠ") in config and config[bstack1ll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧॡ")] == False:
    return False
  else:
    return True
def bstack111ll11_opy_(config, index = 0):
  bstack1ll1ll1_opy_ = {}
  if bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ") in config:
    for bstack1l1llll_opy_ in config[bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index]:
      if bstack1l1llll_opy_ in bstack1llll_opy_ + bstack1ll11_opy_ + [bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ।"), bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ॥")]:
        continue
      bstack1ll1ll1_opy_[bstack1l1llll_opy_] = config[bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ०")][index][bstack1l1llll_opy_]
  for key in config:
    if key in bstack1llll_opy_ + bstack1ll11_opy_ + [bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ१")]:
      continue
    bstack1ll1ll1_opy_[key] = config[key]
  return bstack1ll1ll1_opy_
def bstack111111_opy_(config):
  bstack1l1ll1_opy_ = {}
  for key in bstack1ll11_opy_:
    if key in config:
      bstack1l1ll1_opy_[key] = config[key]
  return bstack1l1ll1_opy_
def bstack111ll1l_opy_(bstack1ll1ll1_opy_, bstack1l1ll1_opy_):
  bstack1111lll_opy_ = {}
  for key in bstack1ll1ll1_opy_.keys():
    if key in bstack11l1l_opy_:
      bstack1111lll_opy_[bstack11l1l_opy_[key]] = bstack1ll1ll1_opy_[key]
    else:
      bstack1111lll_opy_[key] = bstack1ll1ll1_opy_[key]
  for key in bstack1l1ll1_opy_:
    if key in bstack11l1l_opy_:
      bstack1111lll_opy_[bstack11l1l_opy_[key]] = bstack1l1ll1_opy_[key]
    else:
      bstack1111lll_opy_[key] = bstack1l1ll1_opy_[key]
  return bstack1111lll_opy_
def bstack1ll11l11_opy_(config, index = 0):
  caps = {}
  bstack1l1ll1_opy_ = bstack111111_opy_(config)
  if bstack1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ२") in config:
    if bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३") in config[bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ४")][index]:
      caps[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ५")] = config[bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ६")][index][bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ७")]
    if bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ८") in config[bstack1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ९")][index]:
      caps[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ॰")] = str(config[bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॱ")][index][bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॲ")])
    bstack11ll11l_opy_ = {}
    for bstack1ll1l111_opy_ in bstack1ll11_opy_:
      if bstack1ll1l111_opy_ in config[bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॳ")][index]:
        bstack11ll11l_opy_[bstack1ll1l111_opy_] = config[bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॴ")][index][bstack1ll1l111_opy_]
        del(config[bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॵ")][index][bstack1ll1l111_opy_])
    bstack1l1ll1_opy_.update(bstack11ll11l_opy_)
  bstack1ll1ll1_opy_ = bstack111ll11_opy_(config, index)
  if bstack1ll11l1_opy_(config):
    bstack1ll1ll1_opy_[bstack1ll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧॶ")] = True
    caps.update(bstack1l1ll1_opy_)
    caps[bstack1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩॷ")] = bstack1ll1ll1_opy_
  else:
    bstack1ll1ll1_opy_[bstack1ll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩॸ")] = False
    caps.update(bstack111ll1l_opy_(bstack1ll1ll1_opy_, bstack1l1ll1_opy_))
    if bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॹ") in caps:
      caps[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬॺ")] = caps[bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॻ")]
      del(caps[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॼ")])
    if bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॽ") in caps:
      caps[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪॾ")] = caps[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॿ")]
      del(caps[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫঀ")])
  return caps
def bstack11l11ll_opy_():
  if bstack1ll111_opy_() <= version.parse(bstack1ll_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫঁ")):
    return bstack1l1ll_opy_
  return bstack1l11l_opy_
def bstack1ll1l1l1_opy_(options):
  return hasattr(options, bstack1ll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ং"))
def bstack1lllll_opy_(caps):
  browser = bstack1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ঃ")
  if bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ঄") in caps:
    browser = caps[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭অ")]
  elif bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪআ") in caps:
    browser = caps[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫই")]
  browser = str(browser).lower()
  if browser == bstack1ll_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫঈ") or browser == bstack1ll_opy_ (u"ࠬ࡯ࡰࡢࡦࠪউ"):
    browser = bstack1ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ঊ")
  if browser == bstack1ll_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨঋ"):
    browser = bstack1ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨঌ")
  if browser not in [bstack1ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ঍"), bstack1ll_opy_ (u"ࠪࡩࡩ࡭ࡥࠨ঎"), bstack1ll_opy_ (u"ࠫ࡮࡫ࠧএ"), bstack1ll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬঐ"), bstack1ll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧ঑")]:
    return None
  try:
    package = bstack1ll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ঒").format(browser)
    name = bstack1ll_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩও")
    browser_options = getattr(__import__(package, fromlist=[name]), name)
    options = browser_options()
    if not bstack1ll1l1l1_opy_(options):
      return None
    for bstack1l1ll1l_opy_ in caps.keys():
      options.set_capability(bstack1l1ll1l_opy_, caps[bstack1l1ll1l_opy_])
    return options
  except Exception as e:
    logger.debug(str(e))
    return None
def bstack111111l_opy_(options, bstack11ll1ll_opy_):
  if not bstack1ll1l1l1_opy_(options):
    return
  for bstack1l1ll1l_opy_ in bstack11ll1ll_opy_.keys():
    options.set_capability(bstack1l1ll1l_opy_, bstack11ll1ll_opy_[bstack1l1ll1l_opy_])
  if bstack1ll_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨঔ") in options._caps:
    if options._caps[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨক")] and options._caps[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩখ")].lower() != bstack1ll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭গ"):
      del options._caps[bstack1ll_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬঘ")]
def bstack1lll11_opy_(proxy_config):
  if bstack1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫঙ") in proxy_config:
    proxy_config[bstack1ll_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪচ")] = proxy_config[bstack1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ছ")]
    del(proxy_config[bstack1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧজ")])
  if bstack1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧঝ") in proxy_config and proxy_config[bstack1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨঞ")].lower() != bstack1ll_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭ট"):
    proxy_config[bstack1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪঠ")] = bstack1ll_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨড")
  if bstack1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧঢ") in proxy_config:
    proxy_config[bstack1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ণ")] = bstack1ll_opy_ (u"ࠫࡵࡧࡣࠨত")
  return proxy_config
def bstack1l111l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫথ") in config:
    return proxy
  config[bstack1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬদ")] = bstack1lll11_opy_(config[bstack1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ধ")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧন")])
  return proxy
def bstack1lll1l11_opy_(self):
  global CONFIG
  global bstack1ll11l1l_opy_
  if bstack1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ঩") in CONFIG and bstack11l11ll_opy_().startswith(bstack1ll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫপ")):
    return CONFIG[bstack1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧফ")]
  elif bstack1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩব") in CONFIG and bstack11l11ll_opy_().startswith(bstack1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࠨভ")):
    return CONFIG[bstack1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম")]
  else:
    return bstack1ll11l1l_opy_(self)
def bstack1ll1l1ll_opy_():
  if bstack1ll111_opy_() < version.parse(bstack1ll_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧয")):
    logger.warning(bstack11111_opy_.format(bstack1ll111_opy_()))
    return
  global bstack1ll11l1l_opy_
  from selenium.webdriver.remote.remote_connection import RemoteConnection
  bstack1ll11l1l_opy_ = RemoteConnection._get_proxy_url
  RemoteConnection._get_proxy_url = bstack1lll1l11_opy_
def bstack1l1l11_opy_(config):
  if bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭র") in config:
    if str(config[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ঱")]).lower() == bstack1ll_opy_ (u"ࠫࡹࡸࡵࡦࠩল"):
      return True
    else:
      return False
  elif bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࠪ঳") in os.environ:
    if str(os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫ঴")]).lower() == bstack1ll_opy_ (u"ࠧࡵࡴࡸࡩࠬ঵"):
      return True
    else:
      return False
  else:
    return False
def bstack1lll11ll_opy_(config):
  if bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬশ") in config:
    return config[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ষ")]
  if bstack1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩস") in config:
    return config[bstack1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪহ")]
  return {}
def bstack1ll1ll11_opy_(caps):
  global bstack11llll1_opy_
  if bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭঺") in caps:
    caps[bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ঻")][bstack1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ়࠭")] = True
    if bstack11llll1_opy_:
      caps[bstack1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঽ")][bstack1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫা")] = bstack11llll1_opy_
  else:
    caps[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨি")] = True
    if bstack11llll1_opy_:
      caps[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬী")] = bstack11llll1_opy_
def bstack11lll11_opy_():
  global CONFIG
  if bstack1l1l11_opy_(CONFIG):
    bstack11111l1_opy_ = bstack1lll11ll_opy_(CONFIG)
    bstack1l11l11_opy_(bstack11l1l1_opy_(CONFIG), bstack11111l1_opy_)
def bstack1l11l11_opy_(key, bstack11111l1_opy_):
  global bstack1lll1111_opy_
  logger.info(bstack1lll1lll_opy_)
  try:
    bstack1lll1111_opy_ = Local()
    bstack1ll111l1_opy_ = {bstack1ll_opy_ (u"ࠬࡱࡥࡺࠩু"): key}
    bstack1ll111l1_opy_.update(bstack11111l1_opy_)
    logger.debug(bstack1l1l1l1_opy_.format(str(bstack1ll111l1_opy_)))
    bstack1lll1111_opy_.start(**bstack1ll111l1_opy_)
    if bstack1lll1111_opy_.isRunning():
      logger.info(bstack1l1l1ll_opy_)
  except Exception as e:
    bstack1l11111_opy_(bstack1lll11l1_opy_.format(str(e)))
def bstack1lll1ll1_opy_():
  global bstack1lll1111_opy_
  if bstack1lll1111_opy_.isRunning():
    logger.info(bstack111l1l1_opy_)
    bstack1lll1111_opy_.stop()
  bstack1lll1111_opy_ = None
def bstack1111l_opy_():
  logger.info(bstack11lllll_opy_)
  global bstack1lll1111_opy_
  if bstack1lll1111_opy_:
    bstack1lll1ll1_opy_()
  logger.info(bstack11ll11_opy_)
def bstack11l1ll_opy_(self, *args):
  logger.error(bstack1lll11l_opy_)
  bstack1111l_opy_()
def bstack1l11111_opy_(err):
  logger.critical(bstack1lllll1l_opy_.format(str(err)))
  atexit.unregister(bstack1111l_opy_)
  sys.exit(1)
def bstack111l11l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  atexit.unregister(bstack1111l_opy_)
  sys.exit(1)
def bstack1ll11ll1_opy_():
  global CONFIG
  CONFIG = bstack11111ll_opy_()
  CONFIG = bstack1ll1l1l_opy_(CONFIG)
  CONFIG = bstack1lll111_opy_(CONFIG)
  if bstack1l11lll_opy_(CONFIG):
    bstack1l11111_opy_(bstack1ll111l_opy_)
  CONFIG[bstack1ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨূ")] = bstack111l1l_opy_(CONFIG)
  CONFIG[bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪৃ")] = bstack11l1l1_opy_(CONFIG)
  if bstack1lll1l1l_opy_(CONFIG):
    CONFIG[bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫৄ")] = bstack1lll1l1l_opy_(CONFIG)
  bstack11l111l_opy_()
def bstack11l111l_opy_():
  global CONFIG
  global bstack1l1lll1_opy_
  bstack1ll11111_opy_ = 1
  if bstack1ll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ৅") in CONFIG:
    bstack1ll11111_opy_ = CONFIG[bstack1ll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ৆")]
  bstack111l1_opy_ = 0
  if bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧে") in CONFIG:
    bstack111l1_opy_ = len(CONFIG[bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨৈ")])
  bstack1l1lll1_opy_ = int(bstack1ll11111_opy_) * int(bstack111l1_opy_)
def bstack1llll111_opy_(self):
  return
def bstack1111ll_opy_(self):
  return
def bstack1l11l1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1ll1lll_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11ll111_opy_
  global bstack11l1l11_opy_
  global bstack1ll1lll1_opy_
  global bstack1lllll1_opy_
  global bstack11llll_opy_
  global bstack11l11l1_opy_
  CONFIG[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ৉")] = str(bstack11llll_opy_) + str(__version__)
  command_executor = bstack11l11ll_opy_()
  logger.debug(bstack1l1lll_opy_.format(command_executor))
  proxy = bstack1l111l_opy_(CONFIG, proxy)
  bstack1llllll1_opy_ = 0 if bstack11l1l11_opy_ < 0 else bstack11l1l11_opy_
  if bstack1lllll1_opy_ is True:
    bstack1llllll1_opy_ = int(threading.current_thread().getName())
  bstack11ll1ll_opy_ = bstack1ll11l11_opy_(CONFIG, bstack1llllll1_opy_)
  logger.debug(bstack1ll1ll_opy_.format(str(bstack11ll1ll_opy_)))
  if bstack1l1l11_opy_(CONFIG):
    bstack1ll1ll11_opy_(bstack11ll1ll_opy_)
  if options:
    bstack111111l_opy_(options, bstack11ll1ll_opy_)
  if desired_capabilities:
    if bstack1ll111_opy_() >= version.parse(bstack1ll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭৊")):
      desired_capabilities = {}
    else:
      desired_capabilities.update(bstack11ll1ll_opy_)
  if not options:
    options = bstack1lllll_opy_(bstack11ll1ll_opy_)
  if (
      not options and not desired_capabilities
  ) or (
      bstack1ll111_opy_() < version.parse(bstack1ll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧো")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11ll1ll_opy_)
  logger.info(bstack1lll1l_opy_)
  if bstack1ll111_opy_() >= version.parse(bstack1ll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨৌ")):
    bstack11l11l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll111_opy_() >= version.parse(bstack1ll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲্ࠪ")):
    bstack11l11l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11l11l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack11ll111_opy_ = self.session_id
  if bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৎ") in CONFIG and bstack1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ৏") in CONFIG[bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৐")][bstack1llllll1_opy_]:
    bstack1ll1lll1_opy_ = CONFIG[bstack1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৑")][bstack1llllll1_opy_][bstack1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭৒")]
  logger.debug(bstack11l1l1l_opy_.format(bstack11ll111_opy_))
def bstack11lll1l_opy_(self, test):
  global CONFIG
  global bstack11ll111_opy_
  global bstack11111l_opy_
  global bstack1ll1lll1_opy_
  global bstack1llllll_opy_
  if bstack11ll111_opy_:
    try:
      data = {}
      bstack1lll1l1_opy_ = None
      if test:
        bstack1lll1l1_opy_ = str(test.data)
      if bstack1lll1l1_opy_ and not bstack1ll1lll1_opy_:
        data[bstack1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ৓")] = bstack1lll1l1_opy_
      if bstack11111l_opy_:
        if bstack11111l_opy_.status == bstack1ll_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ৔"):
          data[bstack1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ৕")] = bstack1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ৖")
        elif bstack11111l_opy_.status == bstack1ll_opy_ (u"࠭ࡆࡂࡋࡏࠫৗ"):
          data[bstack1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ৘")] = bstack1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ৙")
          if bstack11111l_opy_.message:
            data[bstack1ll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ৚")] = str(bstack11111l_opy_.message)
      user = CONFIG[bstack1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ৛")]
      key = CONFIG[bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧড়")]
      url = bstack1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪঢ়").format(user, key, bstack11ll111_opy_)
      headers = {
        bstack1ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬ৞"): bstack1ll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪয়"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l11ll1_opy_.format(str(e)))
  bstack1llllll_opy_(self, test)
def bstack11lll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack111ll_opy_
  bstack111ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11111l_opy_
  bstack11111l_opy_ = self._test
def bstack1ll11ll_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack1ll_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠣৠ"), bstack1ll_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱࠨৡ"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack1ll_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶࡧ࡭ࡷࠨৢ"), bstack1ll_opy_ (u"ࠦ࠳ࠨৣ")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack1ll_opy_ (u"ࠧ࠰࠮ࡹ࡯࡯ࠦ৤"))))
  if not files:
    pabot._write(bstack1ll_opy_ (u"࠭ࡗࡂࡔࡑ࠾ࠥࡔ࡯ࠡࡱࡸࡸࡵࡻࡴࠡࡨ࡬ࡰࡪࡹࠠࡪࡰࠣࠦࠪࡹࠢࠨ৥") % outs_dir, pabot.Color.YELLOW)
    return bstack1ll_opy_ (u"ࠢࠣ০")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack11l1lll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack1ll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ১") in options:
    del options[bstack1ll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨ২")]
  if ROBOT_VERSION < bstack1ll_opy_ (u"ࠥ࠸࠳࠶ࠢ৩"):
    stats = {
      bstack1ll_opy_ (u"ࠦࡨࡸࡩࡵ࡫ࡦࡥࡱࠨ৪"): {bstack1ll_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࠦ৫"): 0, bstack1ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ৬"): 0, bstack1ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ৭"): 0},
      bstack1ll_opy_ (u"ࠣࡣ࡯ࡰࠧ৮"): {bstack1ll_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࠣ৯"): 0, bstack1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥৰ"): 0, bstack1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦৱ"): 0},
    }
  else:
    stats = {
      bstack1ll_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࠦ৲"): 0,
      bstack1ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ৳"): 0,
      bstack1ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ৴"): 0,
      bstack1ll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤ৵"): 0,
    }
  if pabot_args[bstack1ll_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣ৶")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack1ll_opy_ (u"ࠥࡆࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡤࡘࡕࡏࠤ৷")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack1ll_opy_ (u"ࠦࡦࡸࡴࡪࡨࡤࡧࡹࡹࠢ৸")], pabot_args[bstack1ll_opy_ (u"ࠧࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࡪࡰࡶࡹࡧ࡬࡯࡭ࡦࡨࡶࡸࠨ৹")]
      )
      outputs += [
        bstack1ll11ll_opy_(
          os.path.join(outs_dir, str(index)+ bstack1ll_opy_ (u"ࠨ࠯ࠣ৺")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack1ll_opy_ (u"ࠢࡱࡣࡥࡳࡹࡥࡲࡦࡵࡸࡰࡹࡹࠢ৻"), bstack1ll_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠦࡵ࠱ࡼࡲࡲࠢৼ") % index),
        )
      ]
    if bstack1ll_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࠤ৽") not in options:
      options[bstack1ll_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶࠥ৾")] = bstack1ll_opy_ (u"ࠦࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠣ৿")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1111l11_opy_(self, ff_profile_dir):
  global bstack11l11l_opy_
  if not ff_profile_dir:
    return None
  return bstack11l11l_opy_(self, ff_profile_dir)
def bstack11l1111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11llll1_opy_
  bstack1111l1_opy_ = []
  if bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਀") in CONFIG:
    bstack1111l1_opy_ = CONFIG[bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਁ")]
  bstack1llll1l1_opy_ = len(suite_group) * len(pabot_args[bstack1ll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢਂ")] or [(bstack1ll_opy_ (u"ࠣࠤਃ"), None)]) * len(bstack1111l1_opy_)
  pabot_args[bstack1ll_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣ਄")] = []
  for q in range(bstack1llll1l1_opy_):
    pabot_args[bstack1ll_opy_ (u"ࠥࡆࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡤࡘࡕࡏࠤਅ")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧਆ")],
      pabot_args[bstack1ll_opy_ (u"ࠧࡼࡥࡳࡤࡲࡷࡪࠨਇ")],
      argfile,
      pabot_args.get(bstack1ll_opy_ (u"ࠨࡨࡪࡸࡨࠦਈ")),
      pabot_args[bstack1ll_opy_ (u"ࠢࡱࡴࡲࡧࡪࡹࡳࡦࡵࠥਉ")],
      platform[0],
      bstack11llll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡩ࡭ࡱ࡫ࡳࠣਊ")] or [(bstack1ll_opy_ (u"ࠤࠥ਋"), None)]
    for platform in enumerate(bstack1111l1_opy_)
  ]
def bstack1llll1l_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1l111ll_opy_=bstack1ll_opy_ (u"ࠪࠫ਌")):
  global bstack111l111_opy_
  self.platform_index = platform_index
  self.bstack1l1111l_opy_ = bstack1l111ll_opy_
  bstack111l111_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack111ll1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1111111_opy_
  if not bstack1ll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭਍") in item.options:
    item.options[bstack1ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ਎")] = []
  for v in item.options[bstack1ll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨਏ")]:
    if bstack1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ਐ") in v:
      item.options[bstack1ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ਑")].remove(v)
  item.options[bstack1ll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ਒")].insert(0, bstack1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬਓ").format(item.platform_index))
  item.options[bstack1ll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ਔ")].insert(0, bstack1ll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬਕ").format(item.bstack1l1111l_opy_))
  return bstack1111111_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack111llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1l1l_opy_
  command[0] = command[0].replace(bstack1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਖ"), bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫਗ"), 1)
  return bstack1l1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l111l1_opy_(bstack1lll111l_opy_):
  global bstack11llll_opy_
  bstack11llll_opy_ = bstack1lll111l_opy_
  logger.info(bstack1111ll1_opy_.format(bstack11llll_opy_.split(bstack1ll_opy_ (u"ࠨ࠯ࠪਘ"))[0]))
  global bstack11l11l1_opy_
  global bstack1llllll_opy_
  global bstack111ll_opy_
  global bstack11l11l_opy_
  global bstack1l1l1l_opy_
  global bstack111l111_opy_
  global bstack1111111_opy_
  global bstack1l1ll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack111l11l_opy_(e, bstack111lll_opy_)
  Service.start = bstack1llll111_opy_
  Service.stop = bstack1111ll_opy_
  webdriver.Remote.__init__ = bstack1ll1lll_opy_
  WebDriver.close = bstack1l11l1_opy_
  if (bstack1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨਙ") in str(bstack1lll111l_opy_).lower() or bstack1ll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩਚ") in str(bstack1lll111l_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
    except Exception as e:
      bstack111l11l_opy_(e, bstack111l11_opy_)
    Output.end_test = bstack11lll1l_opy_
    TestStatus.__init__ = bstack11lll1_opy_
    WebDriverCreator._get_ff_profile = bstack1111l11_opy_
  if (bstack1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪਛ") in str(bstack1lll111l_opy_).lower()):
    try:
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack111l11l_opy_(e, bstack11ll1l1_opy_)
    QueueItem.__init__ = bstack1llll1l_opy_
    pabot._create_items = bstack11l1111_opy_
    pabot._run = bstack111llll_opy_
    pabot._create_command_for_execution = bstack111ll1_opy_
    pabot._report_results = bstack11l1lll_opy_
def bstack11l11_opy_(bstack1ll1ll1l_opy_, index):
  bstack1l111l1_opy_(bstack111l_opy_)
  exec(open(bstack1ll1ll1l_opy_).read())
def bstack1l1111_opy_():
  print(bstack11l111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫਜ"), help=bstack1ll_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧਝ"))
  parser.add_argument(bstack1ll_opy_ (u"ࠧ࠮ࡷࠪਞ"), bstack1ll_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬਟ"), help=bstack1ll_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨਠ"))
  parser.add_argument(bstack1ll_opy_ (u"ࠪ࠱ࡰ࠭ਡ"), bstack1ll_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪਢ"), help=bstack1ll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭ਣ"))
  bstack1ll1l11_opy_ = parser.parse_args()
  try:
    bstack1llll11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩਤ"))
    bstack1ll1l11l_opy_ = open(bstack1llll11_opy_, bstack1ll_opy_ (u"ࠧࡳࠩਥ"))
    bstack1ll111ll_opy_ = bstack1ll1l11l_opy_.read()
    bstack1ll1l11l_opy_.close()
    if bstack1ll1l11_opy_.username:
      bstack1ll111ll_opy_ = bstack1ll111ll_opy_.replace(bstack1ll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨਦ"), bstack1ll1l11_opy_.username)
    if bstack1ll1l11_opy_.key:
      bstack1ll111ll_opy_ = bstack1ll111ll_opy_.replace(bstack1ll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫਧ"), bstack1ll1l11_opy_.key)
    file_name = bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ਨ")
    file_path = os.path.abspath(file_name)
    bstack111l1ll_opy_ = open(file_path, bstack1ll_opy_ (u"ࠫࡼ࠭਩"))
    bstack111l1ll_opy_.write(bstack1ll111ll_opy_)
    bstack111l1ll_opy_.close()
    print(bstack1l1l111_opy_)
  except Exception as e:
    print(bstack1l1lllll_opy_.format(str(e)))
def bstack1l11ll_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack1ll11ll1_opy_()
  bstack1lllll11_opy_()
  atexit.register(bstack1111l_opy_)
  signal.signal(signal.SIGINT, bstack11l1ll_opy_)
  signal.signal(signal.SIGTERM, bstack11l1ll_opy_)
def run_on_browserstack():
  if len(sys.argv) <= 1:
    print(bstack1l1l11l_opy_)
    return
  if sys.argv[1] == bstack1ll_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨਪ")  or sys.argv[1] == bstack1ll_opy_ (u"࠭࠭ࡷࠩਫ"):
    print(bstack1ll_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧਬ").format(__version__))
    return
  if sys.argv[1] == bstack1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧਭ"):
    bstack1l1111_opy_()
    return
  args = sys.argv
  bstack1l11ll_opy_()
  global CONFIG
  global bstack1l1lll1_opy_
  global bstack1lllll1_opy_
  global bstack11l1l11_opy_
  global bstack11llll1_opy_
  bstack1ll1111_opy_ = bstack1ll_opy_ (u"ࠩࠪਮ")
  if args[1] == bstack1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪਯ") or args[1] == bstack1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬਰ"):
    bstack1ll1111_opy_ = bstack1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ਱")
    args = args[2:]
  elif args[1] == bstack1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਲ"):
    bstack1ll1111_opy_ = bstack1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਲ਼")
    args = args[2:]
  elif args[1] == bstack1ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ਴"):
    bstack1ll1111_opy_ = bstack1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨਵ")
    args = args[2:]
  elif args[1] == bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫਸ਼"):
    bstack1ll1111_opy_ = bstack1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ਷")
    args = args[2:]
  else:
    if not bstack1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨਸ") in CONFIG or str(CONFIG[bstack1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩਹ")]).lower() in [bstack1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ਺"), bstack1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ਻")]:
      bstack1ll1111_opy_ = bstack1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯਼ࠩ")
      args = args[1:]
    elif str(CONFIG[bstack1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭਽")]).lower() == bstack1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪਾ"):
      bstack1ll1111_opy_ = bstack1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਿ")
      args = args[1:]
    elif str(CONFIG[bstack1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩੀ")]).lower() == bstack1ll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ੁ"):
      bstack1ll1111_opy_ = bstack1ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧੂ")
      args = args[1:]
    else:
      bstack1l11111_opy_(bstack1ll1111l_opy_)
  global bstack11l11l1_opy_
  global bstack1llllll_opy_
  global bstack111ll_opy_
  global bstack11l11l_opy_
  global bstack1l1l1l_opy_
  global bstack111l111_opy_
  global bstack1111111_opy_
  global bstack1l1ll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack111l11l_opy_(e, bstack111lll_opy_)
  bstack11l11l1_opy_ = webdriver.Remote.__init__
  bstack1l1ll11_opy_ = WebDriver.close
  if (bstack1ll1111_opy_ in [bstack1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ੃"), bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ੄"), bstack1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ੅")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
    except Exception as e:
      bstack111l11l_opy_(e, bstack111l11_opy_)
    bstack1llllll_opy_ = Output.end_test
    bstack111ll_opy_ = TestStatus.__init__
    bstack11l11l_opy_ = WebDriverCreator._get_ff_profile
  if (bstack1ll1111_opy_ in [bstack1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ੆"), bstack1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧੇ")]):
    try:
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack111l11l_opy_(e, bstack11ll1l1_opy_)
    bstack1l1l1l_opy_ = pabot._run
    bstack111l111_opy_ = QueueItem.__init__
    bstack1111111_opy_ = pabot._create_command_for_execution
  if bstack1ll1111_opy_ == bstack1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧੈ"):
    bstack11lll11_opy_()
    if bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੉") in CONFIG:
      bstack1lllll1_opy_ = True
      bstack1llll1ll_opy_ = []
      for index, platform in enumerate(CONFIG[bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੊")]):
        bstack1llll1ll_opy_.append(threading.Thread(name=str(index),
                                      target=bstack11l11_opy_, args=(args[0], index)))
      for t in bstack1llll1ll_opy_:
        t.start()
      for t in bstack1llll1ll_opy_:
        t.join()
    else:
      bstack1l111l1_opy_(bstack111l_opy_)
      exec(open(args[0]).read())
  elif bstack1ll1111_opy_ == bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩੋ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack111l11l_opy_(e, bstack111l11_opy_)
    bstack11lll11_opy_()
    bstack1l111l1_opy_(bstack11lll_opy_)
    run_cli(args)
  elif bstack1ll1111_opy_ == bstack1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪੌ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack111l11l_opy_(e, bstack11ll1l1_opy_)
    bstack11lll11_opy_()
    bstack1l111l1_opy_(bstack11l1_opy_)
    if bstack1ll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵ੍ࠪ") in args:
      i = args.index(bstack1ll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ੎"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l1lll1_opy_))
    args.insert(0, str(bstack1ll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ੏")))
    pabot.main(args)
  elif bstack1ll1111_opy_ == bstack1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ੐"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack111l11l_opy_(e, bstack111l11_opy_)
    for a in args:
      if bstack1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨੑ") in a:
        bstack11l1l11_opy_ = int(a.split(bstack1ll_opy_ (u"ࠪ࠾ࠬ੒"))[1])
      if bstack1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ੓") in a:
        bstack11llll1_opy_ = str(a.split(bstack1ll_opy_ (u"ࠬࡀࠧ੔"))[1])
    bstack1l111l1_opy_(bstack11l1_opy_)
    run_cli(args)
  else:
    bstack1l11111_opy_(bstack1ll1111l_opy_)