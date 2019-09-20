#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json
import re
from binascii import b2a_hex, a2b_hex
from utils.helpers import CJsonEncoder
from Crypto.Cipher import AES


class Code:
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.code_text = cryptor.encrypt(text)
        return b2a_hex(self.code_text)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

    def atoi(self, s):
        s = str(s)[::-1]
        num = 0
        for i, v in enumerate(s):
            for j in range(0, 10):
                if v == str(j):
                    num += j * (10 ** i)
        tmp = self.check(str(num))
        num = int(''.join(tmp))
        return num

    def aton(self, s):
        num = ''
        for i, v in enumerate(s):
            for j in range(0, 10):
                if v == str(j):
                    num += str(v)
                    break
            else:
                c = ord(v)
                num += str(c)

        return int(num)

    def check(self, code):
        """获取code的前18位"""
        ereg = re.compile(r"[0-9]{18}")
        return ereg.findall(code)


class MyEncrypt:
    """Encrypt data with AES"""
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
        self.cryptor = AES.new(self.key, self.mode, self.key)

    def encrypt_new(self, text):
        """encrypt json, decrypt with decrypt_new
        text is dict like data(or any can use json.dumps)
        """
        text = json.dumps(text, cls=CJsonEncoder)
        count = len(text)
        length = 16
        add = length - (count % length)
        text = text + ('\0' * add)
        code_text = self.cryptor.encrypt(text)
        data = base64.urlsafe_b64encode(code_text).decode()
        return data

    def decrypt_new(self, text):
        """decrypt json, use with encrypt_new
        text is bytes like or str(auto convert to bytes) like data
        """
        if isinstance(text, str):
            text = text.encode()
        plain_text = self.cryptor.decrypt(base64.urlsafe_b64decode(text)).decode()
        plain_text = plain_text.rstrip('\0')
        plain_text = json.loads(plain_text)
        return plain_text


def phone_2pk(phone_num, key='sinaiftagssinaif'):
    s = Code(key)
    phone_num_encrypt = s.encrypt(str(phone_num))
    pk = s.atoi(phone_num_encrypt)
    return pk


if __name__ == '__main__':
    pk_test = phone_2pk('13928437712')
    print(pk_test)
    d = {
        "code": 200,
        "data": "HAPOElqHBEiW308jzdtV5QilkYsuICbh0xUgm7PJiBJst4mdcnlndxQjPU_EWhcoxX41QyDCciZkPEEsU9knVoGLavOWvJk0mNSv1s0kKyVW0Q-bB45YDSdWh0w9igpbDWgLK3TFCov_RRgBjFs8zZsWmlzcSFKUwYuymhoX43xxSNdp3I6qMaLIUYERG3hLwElM_nlN9g6n9RigW9HULCvzgXfbCfxP89-vunCv2jz860l74qjL_WabjKGB_TZ0I8J988yUloRf7DZUl1pasaf66LZPq2JHYlXAKNKz1GDvdL9kZGGjgdtLfBetfhtN2AisJm5xPbRQh6BAl8wf-hS2g2XStGJSkdf_X3S9RKss6Rm9cPAKv-F-KFFT2jD12qCiASoxwQEbY008qYOmq7u29jBxVcXVc79jlHxiKpJxyqUWzY7jFyH2WUxBUxpbWnsGoloHXmlcoaQ2kjxL8CnDuPxwIms8NEI3IOfDQL20N3bFHXnoCUWlCP7GjMrgBRGICrkoiAfq-tL7y1lZLrD6CqanyP5oeKiIlVC3lJ-LtXB7elvY7mJ7OeJlNyD6sV9Uf5jh6XXbbECMXwBOWaKf299HpFfFoFDgfERJXh_cdKtT8lQA8YYKspnTdFcjTaexQTL4N0j4MdfF0z-RYN8vXIrWbJE0ZGLv89yeqKw-f_sUnv642BoMGoV8gTuaz_RwXc_PhVTvr651uCV9D8TXhd8CVrLtmApyG3hlGi7bodkxo7q5Kc2MDELm5DWB_RdMHuAAebL3JdjiYVHIDy3VUFvMt3H9Bt_mRwsiXNttdM9uIXXQGSJufC61lrmgGtdu9WYTQUdUOymiqcyd_aqA7VaO_9Hr1CktJBJTEg3bcpSnqKM5ctlLslOg4zskUwHG7-rrWus00TLfT2eG0TkUwvHUP40SSB4fHckGrRrwDOkh5lLWoizAblFetx-vHGbnwN8POrUrNpHmKUVZJy_YDSmAIlXPrR8KcYcD4fb-aFB7yc3QXZLFafqhK7-2_3LkvTFYerWy0pFQ5l48_rOIr6QHcFLhknMeJxE1Cf9XPgrL0tp-jX67wYNdaPfS2v76Kiv06Ml7PUii57WFUkXj_TmZLTzCwwAKCEmnjROmRR3d9024-N1bSKD2AVlCgIFBd8ETfc5Oo0SLmHmfUsMoiaKVQORnHxS5nNgcOHBvZYCWf8e1sFaxxpZCxqZ3K0icuwrNRVUCjEg3RIfPiEekfyrok_nh5f_pzYhedJHo_Lwf4D4rSWj_OkZD1rxDpwaRtIdE32QMGji5w1MbX_gok44kfYez-FUZRdxGv5XyEBqe_YraBRBDThBVRH71nRLarHnSBkkhoIpBI5HaqiVnJj_hw-dlaSMQv--3b4EviDf47dzGUZ4WK7Fj9gB0C7PXS6gmTL7RETFhR-YSFsxCRBAgeBG8m3AMsSpPoBTInO1Eo29h05j8Susc-vN0LOaH8Wmp4nHg4ZoTgr7jNxwiGEpziP7SntzL9-QlGx6Rw1w9jNI6y0PMhYohSIR2bmBB8QW0e7qsq_AU7S4kWyeN9ZfSwM6vO9Bl_aEmXDyo-Bk0QACeYWmU0YlSMTaUafwQJze1I8B-gybL0UMkUTHVcQ-k_loUb1u95pbRdUeDeFPxJj99lbW8DoXR8_ZY_AaUCzuemosoGy3BgtpMTJG-S99hEbkHRdMaU8-cRzx73_hi4LGgcvkT1A2ZFLzJMXWMcSbjAhI77kBOgpqtRqFQ7PcRs6mGvUvhkHG_1Kukz6JA8lzN4TYzE0j493HE94Uc2GD5vrdM42npCJZjPw_4ghs6sZ93hfFkXr3dvgygjPJw0zl4iBxONp_RuqAF52x2O3_UL9uaVe3y1nY3mRtQt1zP60mNni0GTsim3nb2b_AnJZXK6kx6_nkS7nSpI-RXvdem77lQyQFTn6WTtdNwxOXHtxbq9pvce1XfWow4W6SITTvIMR6yIfShofma0Cx_web2zPNFU0oG9qX3d3OzH2WuZS06L1y430aVeTuajXs_UO9Q-mn04uL4m9c0whf7XYB5JfMTQ6LHRHV8ROgMmldGEZnko7hQKVsgCi0Odw8GtEcalPCtHYkdxPg-M2vwARqjeorGuUX4HRc84MhuiZm3KCfiwky5AfKS5r5-1TnbuODFEwFFuMzuvQa9IyYR0_7QErQxBtvRoIwZMaNLO8BXM4FjiPOf7lF35vcSR5_wqCZebW-SrJukassDhJHtDfdw4089Z_xUp-XLO5LoqppfMYreUn04_qnqV7aZ0lKzq2Hd07gYLEvhBEWCJXLZniK_OsWXlmrnCxDpW5GGTCJcU7DVHYk2FDhsCEgd-25ZwVLZuXDfN_vLhPyLWLfohGaln1oAG5ibW6rXSgdLF8R2u-7gQQJAwLUQEME9hX0JRBDbQHcViQLbDPtjMIDEPIF_eKsoVKJAYwnQCHnptko_b8cTpWrcfuIucYPaeTKcEKC4fNitlv8hU_fuHtPpL6CKjsg33ptbryb4vXY_kaMdyI09132-dS4eA-nVOSjHtTOsgOaUZkd8Ykj3-rWCjjGlyDXzfZI2q0b3Q9Wtx5UDpNxF8na068nY2u6-rys3C54IBiBoKyyfT5qF6sKO2ruwluxMQAXnzcMlIEiArUy_7RICKGqUY03plgrLAAm2vfXKShixykPJdSJkfm9fdgHtPo5LUZa0mn54Ryep09QzjcYo8F586GUZbpEnmzj0YyyxOffoQ6TM03A2eQQmUPbfHYdKNoA7Szo7oRlFtb1OHJ5-UH_JERszM-L0cvHHnqIWsxiM07BGdPzwQo2NP2QL7DgDtTm9EWtxK65fMtKyjKdHUCctnhzHTpdNoAjGjM_BF_TrJ-HA0q9Cemg2og0_Ab3O90kv3fu7ZIfXwZ_WD2GtmttckXGiVKnm3YDh4qWSyzDf--A_dt41INBlExqprEE6X4Qvskn3LAbaFwT_HqYJ_nRjzxMv3y8Q3nSfxNvS7bwAdd94i3J59cXF_ED2LMBixd6LhNQAkmKbr9U4dD_Ggey-aZuTdXaTZo2HxZOY3AQyE9VgaNrKXKB7E6T9Tc-iXGIzoGwXVzxN1ezEsn4fFib_E2MnJzlXVvMEQQHPK63E8l2Vb5RNBrxHC4vcrW7AxDs8QXId--rdV3oUgRKJCHLo-7evGphaTUM10xe8C1gSPmW2LZt2YTBmC_KEVhKJGZnk-REsRAKgwdWKpnVgkswDfiTG9N_oeJzcmRxgWoECFVAoIOFfWfl4AKQAgD5pYkFixgKGhWNyeIm65KSIMROe5jaDCKcj5xw1BrVo8R1xLoxSbrSNNrrR35ZEMXLAs43ltDwTO3IFGhbZvaRpqYpblXDFkWcFexLQOi1prZAvE865cTY6A0yTk5FF16pvDHlaiPsDylvJVBZUM2bAjpmKSGfkIOWHCDwKWRG9kNiAd-n8WP0HKWGfIQRi9n3pd9eDxO5o5UEHHIQTpyd-KLEJMlu3D-KisEZSQ97m9hNVvcQN8atBixTVTiXMv6cUbjU95phxYRbZ31aCicVFSFTtSqv4PRTEhWYzK4fxx3pJcz8ZWweArYNmF9PXhRUtWJOhmwx8V6mkiJcyclzC1Bun3OXPzlpG1CgitSAJfljIyhZb88eykyP1KnkWBs77CpNSqXxAhX74a_o0No6behLtKZC2mX35eNTjCCsXkKwBluIuJsuX",
        "message": "查询标签成功"
    }
    d_f = {
        "code": 200,
        "data": "cRL6UzZVRii_3LpXMpD6p6pL_AZnexmfriUvcncQK3Ju2FcOGbC5GZJBaap8Y4ZV",
        "message": "ok"
    }
    met = MyEncrypt(key='label13929422445')
    print(met.decrypt_new(d['data']))
    met1 = MyEncrypt(key='score15874426600')
    print(met1.decrypt_new(d_f["data"]))
