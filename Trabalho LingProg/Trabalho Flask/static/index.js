// tudo isso pra deletar uma anotacao
function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) =>{
        window.location.href = "/";
    });
}