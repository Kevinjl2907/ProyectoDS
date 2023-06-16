import CryptoJS from "crypto-js";
import Config from "@/service/config";

const md5Encrypt = (ptext_to_encrypt) => {
	let encrypt = CryptoJS.MD5(ptext_to_encrypt);
	//console.log(`Encriptado MD5: ${encrypt}`);
	return encrypt;
};

const sha256Encrypt = (ptext_to_encrypt) => {
	let encrypt = CryptoJS.SHA256(ptext_to_encrypt);
	//console.log(`Encriptado SHA256: ${encrypt}`);
	return encrypt;
};

const aesEncrypt = (ptext_to_encrypt) => {
	let data = ptext_to_encrypt;
	//let	salt = CryptoJS.SHA256( "Salt" );
	//let	iv   = CryptoJS.SHA1( "Vector" );
	//let	key  = CryptoJS.SHA256( "Key" );
	let salt = CryptoJS.SHA256(Config.SecretKey.aes_SALT);
	let iv = CryptoJS.SHA1(Config.SecretKey.aes_IV);
	let key = CryptoJS.SHA256(Config.SecretKey.aes_KEY);

	// Prepare substances
	salt = salt.toString(CryptoJS.enc.Base64);
	iv = iv.toString(CryptoJS.enc.Base64).substr(0, 16);
	//console.log(`ivb64: ${iv}`);
	iv = CryptoJS.enc.Utf8.parse(iv);
	//console.log(`ivParsed: ${iv}`);
	key = key.toString(CryptoJS.enc.Base64).substr(0, 32);
	//console.log(`keyb64: ${key}`);
	key = CryptoJS.enc.Utf8.parse(key);
	//console.log(`keyParsed: ${key}`);
	data = salt + data;
	// Cipher
	//let encrypted = CryptoJS.AES.encrypt( salt + data, key, { iv: iv });
	let encrypted = CryptoJS.AES.encrypt(data, key, { iv: iv });

	// Results
	//console.log( "SALT\n"       + salt );
	//console.log( "IV\n"         + encrypted.iv.toString( CryptoJS.enc.Utf8 ));
	//console.log( "KEY\n"        + encrypted.key.toString( CryptoJS.enc.Utf8 ));
	//console.log( "ENCRYPTED\n"  + encrypted.toString());

	return encrypted.toString();
};

const aesDecrypt = (ptext_to_decrypt) => {
	//console.log(ptext_to_decrypt);
	//console.log(typeof(ptext_to_decrypt));
	let decrypted = null;
	let data = ptext_to_decrypt || "vacio";
	if (data != "vacio") {
		data = data.toString();
		//console.log({data});
		//let	salt = CryptoJS.SHA256( "Salt" );
		//let	iv   = CryptoJS.SHA1( "Vector" );
		//let	key  = CryptoJS.SHA256( "Key" );
		let salt = CryptoJS.SHA256(Config.SecretKey.aes_SALT);
		let iv = CryptoJS.SHA1(Config.SecretKey.aes_IV);
		let key = CryptoJS.SHA256(Config.SecretKey.aes_KEY);

		// Prepare substances
		salt = salt.toString(CryptoJS.enc.Base64);
		iv = iv.toString(CryptoJS.enc.Base64).substr(0, 16);
		//console.log(`ivb64-decrypt: ${iv}`);
		iv = CryptoJS.enc.Utf8.parse(iv);
		//console.log(`ivParsed-decript: ${iv}`);
		key = key.toString(CryptoJS.enc.Base64).substr(0, 32);
		//console.log(`keyb64-decript: ${key}`);
		key = CryptoJS.enc.Utf8.parse(key);
		//console.log(`keyParsed-decript: ${key}`);
		//
		// Cipher
		//let encrypted = CryptoJS.AES.decrypt(salt + data, key, { iv: iv });
		//console.log('Desencriptar:\n' + data);
		decrypted = CryptoJS.AES.decrypt(data, key, { iv: iv });
		decrypted = CryptoJS.enc.Utf8.stringify(decrypted).toString();
		decrypted = decrypted.substr(salt.length);
		//console.log("Decripted\n" + decrypted);
		//console.log(decrypted);
		// Results
		//console.log( "SALT\n"       + salt );
		//console.log( "IV\n"         + decrypted.iv.toString( CryptoJS.enc.Utf8 ));
		//console.log( "KEY\n"        + decrypted.key.toString( CryptoJS.enc.Utf8 ));
		//console.log( "DECRYPTED\n"  + decrypted.toString());
	}
	//return decrypted.toString();
	return decrypted;
};

export default {
	md5Encrypt,
	sha256Encrypt,
	aesEncrypt,
	aesDecrypt,
};
