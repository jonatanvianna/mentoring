//TODO - a data vem do server com String, preciso ver ou como internacionalizar ou como formatar
// No mongo a data está como um objeto "birth_date" : ISODate("1950-03-30T00:00:00Z")


function Char(props){
   const char = props.char;
   char.playable = char.playable == true ? "playable" : "Not playable";
   console.log(typeof(char.birth_date));
      return (
         <article className="media">
            <figure className="media-left">
               <p className="image is-128x128">
                  <img src="celes_chere.png"/>
               </p>
            </figure>
            <div className="char" className="media-content">
               <div  className="content">
                  <p>
                     <strong>{char.name} {char.surname}</strong><br/>
                     {char.species}, Born in {char.birth_date},<br />
                     Is a {char.playable} character from {char.game} game.<br />
                     <small>
                        Life status: health: {char.health}, mana: {char.health}<br />
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


function getChar(){
      return axios.get('http://127.0.0.1:5000/character/Celes')
        .then(function (r){
          const char = r.data.result;
            console.log(char.birth_date);
            console.log(typeof(char.birth_date));
             ReactDOM.render(<Char char={char}/>,
               document.getElementById('chars')
            );
        })
        .catch(function (e){
          return e;
        });
   }

function getAllChars(){
   var char = getChar();
}