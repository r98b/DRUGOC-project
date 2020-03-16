import React from 'react'

class Introduction extends React.Component{
    constructor(props){
        super(props);

    }
    render(){
        return(
            <div className={this.props.status?'hide':"Intro"}>
            <h3>Welcome</h3>
            <p>
            DrugOC est un outil informatique innovant destiné au suivi de la pharmacovigilance en regroupant les déclarations volontaires des praticiens professionnel de santé et/ou patients qui rencontrent des effets indésirables dû à la prise d'un médicament. L’ensemble de manière simple, complète et rapide, en prenant en compte l’ensemble des paramètres et variables nécessaires. DrugOC facilite la collecte et la soumission des données au CNPM en substituant ainsi le travail des centres régionaux.
            </p>
            <button 
            id="btn" 
            style={{backgroundColor:'rgba(19, 177, 205, 0.95)',color:'white'}}
            onClick={this.props.handleClick}
            >
                Next
            </button>
            </div>
        )
    }
}
export default Introduction;