#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
La-Mulana Remake language .dat file encoder and decoder.
The original script was downloaded from the La-Muana Wikia: http://lamulana-remake.wikia.com/wiki/Text_Dump
Encoding support added by Alexei Baboulevitch.
Modding support added by Smurfton.
"""

import os, codecs, re, unicodedata, mmap

font00 = \
        u"!\"&'(),-./0123456789:?ABCDEFGHIJKLMNOPQRSTUVWXYZ"\
        u"　]^_abcdefghijklmnopqrstuvwxyz…♪、。々「」ぁあぃいぅうぇえぉおか"\
        u"がきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほ"\
        u"ぼぽまみむめもゃやゅゆょよらりるれろわをんァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセ"\
        u"ゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリル"\
        u"レロワヲンヴ・ー一三上下不与世丘両中丸主乗乙乱乳予争事二人今介仕他付代以仮仲件会伝位低住体何作使"\
        u"供侵係保信俺倍倒値偉側偶備傷像僧元兄先光兜入全公具典内再冒冥出刀分切列初別利刻則前剣創力加助効勇"\
        u"勉動化匹十半協博印危去参双反取受叡口古召可台史右司合同名向否周呪味呼命品唯唱問喜営器噴四回囲図国"\
        u"土在地坂型域基堂報場塊塔墓増壁壇壊士声売壷変外多夜夢大天太央失奇契奥女好妊妖妻始姿娘婦子字存孤学"\
        u"宇守官宙定宝実客室宮家密寝対封専導小少尾屋屏属山岩崖崩嵐左巨己布帯帰常年幸幻幾広床底店度座庫廊廟"\
        u"弁引弟弱張強弾当形影役彼待後心必忍忘応念怒思急性怨恐息恵悔悟悪悲情惑想意愚愛感慈態憶我戦戻所扉手"\
        u"扱投抜押拝拡拳拾持指振探撃撮操支攻放敗教散数敵敷文料斧断新方旅族日早昇明昔星映時晩普晶智暗曲書最"\
        u"月有服望未末本杉村杖束来杯板析果架柱査格械棺検椿楼楽槍様槽模樹橋機欠次欲歓止正武歩歯歳歴死殊残段"\
        u"殺殿母毒毛気水氷永求汝池決治法波泥注洞洪流海消涙涯深済減湖満源溶滅滝火灯灼炎無然熱爆爪父版牛物特"\
        u"犬状狂独獄獅獣玄玉王珠現球理瓶生産用男画界略番発登白百的盤目直盾看真眼着知石研破碑示礼社祈祖神祠"\
        u"祭禁福私秘秤移種穴究空突窟立竜章竪端笛符第筒答箱範精系約納純紫細紹終経結続緑練罠罪罰義羽習翻翼老"\
        u"考者耐聖聞肉肩胸能脱腕自至船色若苦英荷華落葉蔵薇薔薬蛇血行術衛表裁装裏補製複要見覚親解言記訳証試"\
        u"話詳認誕誘語誠説読誰調論謁謎謝識議護谷貝財貧貯買貸資賢贄贖赤走起超足跡路踊蹴身車軽輝辞込辿近返迷"\
        u"追送逃通速造連進遊過道達違遠適選遺還郎部配重野量金針鉄銀銃銅録鍵鎖鏡長門閉開間関闇闘防限険陽階隠"\
        u"雄雑難雨霊青静面革靴音順領頭題顔願類風飛食館馬駄験骨高魂魔魚鳥鳴黄黒泉居転清成仏拠維視宿浮熟飾冷"\
        u"得集安割栄偽屍伸巻緒捨固届叩越激彫蘇狭浅Ⅱ［］：！？～／０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪ"\
        u"ＫＬＭＮＯＰＲＳＴＵＶＷＸＹａｂｄｅｇｈｉｌｍｏｐｒｓｔｕｘ辺薄島異温復称狙豊穣虫絶ＱＺｃｆｊｋ"\
        u"ｎｑｖｗｙｚ＋－旧了設更橫幅似確置整＞％香ü描園為渡象相聴比較掘酷艇原民雷絵南米平木秋田県湯環砂"\
        u"漠角運湿円背負構授輪圏隙草植快埋寺院妙該式判（）警告収首腰芸酒美組各演点勝観編丈夫姫救’，．霧節"\
        u"幽技師柄期瞬電購任販Á;û+→↓←↑⓪①②③④⑤⑥⑦⑧⑨<”挑朝痛魅鍛戒飲憂照磨射互降沈醜触煮疲"\
        u"素競際易堅豪屈潔削除替Ü♡*$街極"

def decode_block(b):
    b = list(b)
    d = ""
    while b:
        o = ord(b.pop(0))
        if o == 0x000A:
            s = "{0x%04x}\n" % o
        elif o in [0x000C, 0x0020]:
            # handles FORM FEED, SPACE 
            if (o == 0x000C):
                s = "{FF}"
            else:
                s = chr(o)
        elif o >= 0x0040 and o <= 0x0050:
            s = ""
            if o == 0x0040:
                cmd = "{FLAG %x:=%x}" % (ord(b[0]), ord(b[1]))
                b = b[2:]
            elif o == 0x0042:
                cmd = "{ITEM %x}" % ord(b[0])
                b = b[1:]
            elif o == 0x0044:
                cmd = "{CLS}\n\n"
            elif o == 0x0045:
                cmd = "\n"
            elif o == 0x0046:
                cmd = "{POSE %x}" % ord(b[0])
                b = b[1:]
            elif o == 0x0047:
                cmd = "{MANTRA %x}" % ord(b[0])
                b = b[1:]
            elif o == 0x004a:
                colors = [ord(x) for x in b[:3]]
                cmd = "{COL %02x-%02x-%02x}" % tuple(colors)
                b = b[3:] #TODO: colors not verified
            elif o == 0x004e:
                lenopts = ord(b[0])
                opts = ["%04x" % ord(x) for x in b[1:lenopts+1]]
                cmd = "{CMD %s}" % "-".join(opts)
                b = b[lenopts+1:]
            elif o == 0x004f:
                cmd = "{SCENE %x}" % ord(b[0])
                b = b[1:]
            else:
                cmd = "{0x%04x}" % o
                # assert False # nope.
                print("Unrecognized character.")
            s = cmd
        elif o >= 0x0100 and o <= 0x05c0:
            s = font00[o-0x0100]
        elif o == 0x05c1:
            s = "{UN}"
        elif o == 0x05c2:
            s = "{DEFI}"
        elif o == 0x05c3:
            s = "{NED}"
        else:
            s = "{0x%04x}" % o
            # assert False # nope.
            print("Unrecognized character.")
        d += s
    return d

def encode_block(block):
	
    special_regex = r"^{([a-zA-Z]+)(\s(.*?))?}"
    flag_regex = r"([0-9a-fA-F]+):=([0-9a-fA-F]+)"
    color_regex = r"([0-9a-fA-F]+)-([0-9a-fA-F]+)-([0-9a-fA-F]+)"
    cmd_regex = r"([0-9a-fA-F]+)-?"
    hex_regex = r"^{(?:0x)?([0-9a-fA-F]{1,4})}"
    newline_regex = "^\n*"
    output = []
    count = 0

    while len(block) > 0:
        match = re.match(special_regex, block)
        hex_match = re.match(hex_regex, block)
        # lenbuf is used for when commands get filler after them (for readability)
        lenbuf = 0
        if match is not None:
            command = match.group(1)
            parameters = match.group(3)

            if command == "FF":
                output.append(0x000C)
            elif command == "FLAG":
                param_match = re.match(flag_regex, parameters)
                assert param_match is not None

                output.append(0x0040)
                output.append(int(param_match.group(1), base=16))
                output.append(int(param_match.group(2), base=16))
            elif command == "ITEM":
                output.append(0x0042)
                output.append(int(parameters, base=16))
            elif command == "CLS":
                output.append(0x0044);
                newline_match = re.match(newline_regex, block[len(match.group(0)):])
                lenbuf = len(newline_match.group(0))
            elif command == "POSE":
                output.append(0x0046)
                output.append(int(parameters, base=16))
            elif command == "MANTRA":
                output.append(0x0047)
                output.append(int(parameters, base=16))
            elif command == "COL":
                param_match = re.match(color_regex, parameters)
                assert param_match is not None

                output.append(0x004a)
                output.append(int(param_match.group(1), base=16))
                output.append(int(param_match.group(2), base=16))
                output.append(int(param_match.group(3), base=16))
            elif command == "CMD":
                command_output = []
                command_output.append(0x004e)
                count = 0

                while len(parameters) > 0:
                    param_match = re.match(cmd_regex, parameters)
                    assert param_match is not None

                    command_output.append(int(param_match.group(1), base = 16))
                    parameters = parameters[len(param_match.group(0)):]
                    count += 1

                command_output.insert(1, count)

                output += command_output

                # Only used to start credits
            elif command == "SCENE":
                output.append(0x004f)
                output.append(int(parameters, base=16))
            elif command == "UN":
                output.append(0x05c1)
            elif command == "DEFI":
                output.append(0x05c2)
            elif command == "NED":
                output.append(0x05c3)
            
            # not handling UNK characters since they haven't appeared in my input
            # Handling UNK characters for modding purposes. -Smurfton

            block = block[len(match.group(0)) + lenbuf:]
            
        
        elif hex_match is not None:
            output.append(int(hex_match.group(1), base=16))
            
            if int(hex_match.group(1), base=16) == 0x0A:
                newline_match = re.match(newline_regex, block[len(hex_match.group(0)):])
                lenbuf = len(newline_match.group(0))
                    
            block = block[len(hex_match.group(0)) + lenbuf:]
        elif block[0] == '\n':
            output.append(0x0045);
            block = block[1:]
        else:
            char_ord = ord(block[0])

            location_in_font = font00.find(block[0:1])
            if location_in_font != -1:
                output.append(location_in_font + 0x0100)
            else:
                output.append(char_ord)

            block = block[1:]

    return output


def decode(fin, fout):
    # first character = number of blocks
    blocks = ord(fin.read(1))
    count = 0
    
    c = fin.read(1)
    while c:
        # each block starts with the number of characters in it x 2
        o = ord(c)
        assert o % 2 == 0

        b = fin.read(o//2)

        block_header = "-" * 40 + " " + "BLOCK %x (%x) START" % (count, o//2)
        block_footer = "-" * 40 + " " + "BLOCK %x END" % (count)

        fout.write("%s\n%s\n%s\n" % (block_header, decode_block(b), block_footer))
        
        count += 1
        c = fin.read(1)
    assert count == blocks

def encode(fin, fout):
    block_regex = r"-+ BLOCK ([0-fA-F]+) \(([0-fA-F]+)\) START\n(.*?)\n-+ BLOCK ([0-fA-F]+) END"

    fin_string = linestring = fin.read();
    block_matches = re.findall(block_regex, fin_string, re.DOTALL)

    last_block_number = int(block_matches[-1][0], 16) + 1
    assert len(block_matches) == last_block_number

    encoded_blocks = [len(block_matches)]

    for block_match in block_matches:
        block_num = int(block_match[0], 16)
        block_len = int(block_match[1], 16)
        block_end_num = int(block_match[3], 16)

        assert block_num == block_end_num

        encoded_block = encode_block(block_match[2])
        encoded_block.insert(0, len(encoded_block) * 2)

        encoded_blocks += encoded_block

    
    encoded_blocks_string = ""

    for char in encoded_blocks:
        encoded_blocks_string += chr(char)

    fout.write(encoded_blocks_string)


dir_ = os.path.dirname(__file__)
if not os.path.exists(os.path.join(dir_, "out")):
    os.makedirs(os.path.join(dir_, "out"))
try:    
    with codecs.open("script_out.txt", "r", "utf_8") as fin:
        with codecs.open(os.path.join(dir_,"out","script_code.dat"), "w", "utf_16_be") as fout:
            encode(fin, fout)
    print("Encoded.")
except:
    print("Did Not Encode")
try:
    with codecs.open("script_code.dat", "r", "utf_16_be") as fin:
        with codecs.open(os.path.join(dir_,"out","script_out.txt"), "w", "utf_8") as fout:
            decode(fin, fout)
    print("Decoded.")
except:
    print("Did Not Decode")

