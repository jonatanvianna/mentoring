


function clique(){
var result = document.getElementById("chars");
result.innerHTML = '';

axios.get('http://127.0.0.1:5000/character/Celes')
  .then(function (r){
    console.log(r.data);
    result.innerHTML = '<pre>' + JSON.stringify(r.data.result, null, '\t') + '</pre>'
  })
  .catch(function (e){
    console.log(e);
  });
}



