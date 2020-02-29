function saveBook() {
	var data = document.getElementById("data").value
	var url = document.getElementById("dataURL").value
	eel.save_book(data, url)

	document.getElementById("text").innerHTML = "Kniha " + data + " byla přidána do databáze."

    document.getElementById("data").value = ""
    document.getElementById("dataURL").value = ""
}
