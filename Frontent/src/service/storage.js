import config from "@/service/config";
import Cripto from "@/service/Cripto";

const setStorage = (key, value, storage = config.globales.Storage) => {
	let now = new Date();
	let Encrypt = null;
	let vkey = key || "vacio";
	let vitem = value || "vacio";
	if (vitem != "vacio" && vkey != "vacio") {
		Encrypt = Cripto.aesEncrypt(value);
		let expira = now.getTime() + config.globales.Storage_expira * 60 * 60 * 1000; // Se suma en milisegundos.
		const sub_item = {
			data: Encrypt,
			expira: expira,
		};
		if (storage === "Local") {
			localStorage.setItem(key, JSON.stringify(sub_item));
		} else {
			sessionStorage.setItem(key, JSON.stringify(sub_item));
		}
	}
	return Encrypt;
};
const getStorage = (key, where = "general", storage = config.globales.Storage) => {
	// Si where viene con '' significa que es un item particular, es decir, no está dentro de conjunto de valores
	let decrypt = null;
	let vkey = key || "vacio";
	let vkey_global = vkey;
	//
	if (vkey != "vacio") {
		if (where) {
			vkey = where;
		}
		if (storage === "Local") {
			vkey = localStorage.getItem(vkey);
		} else {
			vkey = sessionStorage.getItem(vkey);
		}
		if (!vkey) {
			return null;
		}
		let item = JSON.parse(vkey);
		const now = new Date();
		if (now.getTime() > item.expira) {
			removeStorage(vkey, storage);
			return null;
		}
		if (item) {
			decrypt = Cripto.aesDecrypt(item.data);
		}
		if (where) {
			let lresponse = JSON.parse(decrypt);
			decrypt = lresponse[0][vkey_global];
		}
	}
	return decrypt;
};
const getAllStorage = (key, storage = config.globales.Storage) => {
	let decrypt = null;
	let vkey = key || "vacio";
	//
	if (vkey != "vacio") {
		if (storage === "Local") {
			vkey = localStorage.getItem(vkey);
		} else {
			vkey = sessionStorage.getItem(vkey);
		}
		if (!vkey) {
			return null;
		}
		let item = JSON.parse(vkey);
		const now = new Date();
		if (now.getTime() > item.expira) {
			removeStorage(vkey, storage);
			return null;
		} else {
			decrypt = JSON.parse(Cripto.aesDecrypt(item.data));
		}
	}
	return decrypt;
};
const removeStorage = (key, storage = config.globales.Storage) => {
	if (storage === "Local") {
		localStorage.removeItem(key);
	} else {
		sessionStorage.removeItem(key);
	}
};
const clearStorage = (storage = config.globales.Storage) => {
	if (storage === "All") {
		localStorage.clear();
		sessionStorage.clear();
	} else if (storage === "Local") {
		localStorage.clear();
	} else {
		sessionStorage.clear();
	}
};

export default {
	setStorage,
	getStorage,
	getAllStorage,
	removeStorage,
	clearStorage,
};
