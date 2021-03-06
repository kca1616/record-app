import { useEffect, useState } from "react";
import { useHistory } from 'react-router-dom';
import { getFavorites, deleteFavorite } from "../services";

const Wishlist = (props) => {
    const [favorites, setFavorites] = useState([]);
    const history = useHistory();
    const records = favorites.map(fave => fave.record);

    useEffect(() => {
        if (props.user) {
            getFavorites().then((fetchedFavorites) => setFavorites(fetchedFavorites));
        }

    }, []);

    const handleDelete = async (record) => {
        await deleteFavorite(record);
        history.push('/')
    }

    return (
        <section>
            {records.length ?
                records.map((record) => (
                    <div className="record-library">
                        <img src={record.album_art} alt="album cover art"></img>
                        <h3>{record.name}</h3>
                        <h4>{record.year_pressed}</h4>
                        <h5>{record.catalog_number}</h5>
                        <button onClick={() => handleDelete(record.id)}>Delete</button>
                    </div>
                )) : <p>Wishlist is empty.</p>}
        </section>
    )
}

export default Wishlist;