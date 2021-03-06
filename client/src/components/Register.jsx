import { useState } from "react";
import { register } from "../services"
import { useHistory } from 'react-router-dom';

const Register = (props) => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [err, setErr] = useState("");
    const history = useHistory();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const newUser = {
            username,
            email,
            password,
        };
        console.log(newUser);
        const user = await register(newUser).catch((err) => err);
        console.log(user);
        if (user?.message) {
            setErr("A user with this username or email already exists.");
        } else {
            props.setUser(user);
            history.push('/');
        }

    }

    return (
        <section>
            <h3>Register</h3>
            <form className="register" onSubmit={handleSubmit}>
                <label htmlFor="username">Username:</label>
                <input
                    id="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <label htmlFor="email">Email:</label>
                <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <label htmlFor="password">Password:</label>
                <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Sign up!</button>
                <p>{err}</p>

            </form>
        </section>
    );
};

export default Register;