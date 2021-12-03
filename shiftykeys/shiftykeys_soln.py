import hashlib
from base64 import b64encode, b64decode
from Crypto.Cipher import AES

# In the key exchange y is calculated as (self.g * self.x) % self.p

# We know g and p so just get the mod multiplication inverse of g as pow(g,-1,p) and multiply by p to get x

# Then get key as othery*x %p and decrypt the message

g = 3
p = 0xf66a1d0b27dd06c0c24b43030fa04963517942744a68004da3b01b6a999783e8001a4eb8182202c805b20e40c22fbbf05156aca964cb355d8248d9ac2547f307a5bdaaac0b29a06f3e1f11d0bb9985564887ae686e8726bf43f75ea1d99a26227f5daaac0b29a06f3e1f11d0bb9985564887ae686e8726bf43f75ea1d99a26227f507e5fb40d8d3e5d98d2c1f61e78e6098e232c7224d0d666d3231c7a56cb3c4d407e5fb40d8d3e5d98d2c1f61e78e6098e232c7224d0d666d3231c7a56cb3c4d402df1dd6112aba6fc2a85f271328de1c4e88edfa833bd5ddf829b5a6ddad677802df1dd6112aba6fc2a85f271328de1c4e88edfa833bd5ddf829b5a6ddad677
a = 937851173926924342648988403569237370496530291875078822017528790208672675753488686928287980680633563110546149077869725549116657809798878396128997490502544326396790864475176403326396107805000677432762337736259965617202022588727970407516892554724329653947641436056375912704476725966245286218046132976745456446053130181662347649542138274906680134661978084121251991305576823042063463220876958386811356211899877797568828437137315110195260570432706343368525313082725889860943973300956623215749547410275747949196695408996973548573566316635420823147522626738968535270559727644883968648453114449200971667538034104326404857928234
b = 5621536441835989719151803419685834632618083160098500201191695860960723679250308255390753426802083042934378403631793410644808316182908260380617241671430559936456526583126874128191732126381494432205894542613888609161408671462150283726850250084310837792439812223735998170267784395106678940684992231617239495965054918788935567067645736214875899283710864760015183174764573996143573098411933072472168214256932211996273274175237409080236172232312761614320700513342773604922038473522668071395130755361818726244340726662695108549522971385682807074188124556969819838435147468732437640594390657323547587510652851431389272130317576
message = "u7rsxUHdLwdZJ9hdJ5RljfzqE2Krr9DUH+v318n40RL1Ayd0PI5sk94M/WZP+u6yR4mCp3Ab1/rLDwLURt9PHg=="


if __name__ == "__main__":
    y_server = a
    y_client = b

    g_inv = pow(g, -1, p)
    x = y_server*g_inv % p

    key = str(y_client*x % p)
    iv = key[0:16]
    key = bytes(hashlib.md5(bytes(key, "utf-8")).hexdigest(), "utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv=bytes(iv, "utf-8"))
    plain = cipher.decrypt(b64decode(message))
    print(plain)
