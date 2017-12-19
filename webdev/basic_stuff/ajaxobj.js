xmlhttp=createobj();

function createobj() {
	if(window.XMLHttpRequest) {
		return new XMLHttpRequest();
	}
	return new ActiveXObject('Microsoft.XMLHttp');
}