import { createSlice } from '@reduxjs/toolkit';

const auth_initial_state = {
    user_id: null,
    fullname: null,
    username: null,
    email: null,
    token: null,
    is_authenticated: false,
};

export const authenticationSlice = createSlice({
    name: 'userAuthentication',
    initialState: auth_initial_state,
    reducers: {
        addUser: (state, action) => {
            const { user_id, fullname, username, email, token } =
                action.payload;
            state.user_id = user_id;
            state.fullname = fullname;
            state.username = username;
            state.email = email;
            state.token = token;
            state.is_authenticated = true;

            localStorage.setItem('userAuthentication', JSON.stringify(state));
        },
        removeUser: (state) => {
            state.user_id = null;
            state.fullname = null;
            state.username = null;
            state.email = null;
            state.token = null;
            state.is_authenticated = false;
            localStorage.removeItem('userAuthentication');
        },
    },
});

export const { addUser, removeUser } = authenticationSlice.actions;
export default authenticationSlice.reducer;
