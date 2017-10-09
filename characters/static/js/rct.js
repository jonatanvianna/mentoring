

//TODO - a data vem do server com String, preciso ver ou como internacionalizar ou como formatar
// No mongo a data está como um objeto "birth_date" : ISODate("1950-03-30T00:00:00Z")




function Char(char){

   if (typeof(char.char) === 'object'){
      var char = char.char
   }
   var isPlayable  = char.playable == true ? "playable" : "non playable";

      return (
         <article className="media">
            <figure className="media-left">
               <p className="image is-128x128">
                  <img src={char.picture_path + char.picture_file}/>
               </p>
            </figure>
            <div className="char" className="media-content">
               <div  className="content">
                  <input type="hidden" value={char._id.$oid} />
                  <p>
                     <strong>{char.name} {char.surname}</strong><br/>
                     {char.species}, Born in {char.birth_date.$date},<br />
                     Is a {isPlayable} character from {char.game} game.<br />
                     <small>
                        Life status: health: {char.health}, mana: {char.mana}<br />
                        Have: {char.gold_pieces} GP
                     </small>
                  </p>
               </div>
               <nav className="level is-mobile">
                  <div className="level-left">
                     {/*Nothing*/}
                  </div>
               </nav>
            </div>
            <div className="media-right">
               <a className="level-item">
                  <span className="icon"><i className="fa fa-times-rectangle"></i></span>
               </a>
               <a className="level-item">
                  <span className="icon"><i className="fa fa-pencil-square-o"></i></span>
               </a>
               <a className="level-item">
                  <span className="icon"><i className="fa fa-heart"></i></span>
               </a>
               <a className="level-item">
                  <span className="icon"><i className="fa fa-mail-forward"></i></span>
               </a>
            </div>
         </article>

      );
}


function CharList(props) {
   var chars = props.chars;

  return (
     <div>
        {chars.map(
            (char) =>
               <Char
                  key = {char._id}
                  picture_path = {char.picture_path}
                  picture_file = {char.picture_file}
                  name = {char.name}
                  surname = {char.surname}
                  species= {char.species}
                  birth_date = {char.birth_date}
                  playable = {char.playable}
                  game = {char.game}
                  health = {char.health}
                  mana = {char.mana}
                  gold_pieces = {char.gold_pieces}
                />
            )}
     </div>
  );
}


function getAllChars(){
   return axios.get('http://127.0.0.1:5000/characters')
      .then(function (r){
         let chars = r.data;
         ReactDOM.render(
            <CharList chars={chars}/>,
            document.getElementById('chars')
         );
      })
      .catch(function (e){
         return e;
      });
}

function getChar(){
   return axios.get('http://127.0.0.1:5000/characters/59daa2f4ddea8f627c1b13b8')
      .then(function (r){
      console.log(r.data)
         ReactDOM.render(
            <Char char={r.data} />,
            document.getElementById('chars')
         );
      })
      .catch(function (e){
         return e;
      });
}
