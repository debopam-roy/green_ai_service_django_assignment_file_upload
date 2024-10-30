import { configureStore } from '@reduxjs/toolkit';
import authenticationSlice from '../features/authentication/authenticationSlices';

const loadStateFromLocalStorage = () => {
    try {
        const serializedState = localStorage.getItem('userAuthentication');
        if (serializedState === null) return undefined;
        return JSON.parse(serializedState);
    } catch (err) {
        console.error('Could not load state from localStorage', err);
        return undefined;
    }
};

const saveState = (state) => {
    try {
        const serializedState = JSON.stringify(state);
        localStorage.setItem('userAuthentication', serializedState);
    } catch (err) {
        console.error('Could not save state', err);
    }
};

const preloadedState = loadStateFromLocalStorage() || {
    userAuthentication: {
        user_id: null,
        fullname: null,
        username: null,
        email: null,
        token: null,
        is_authenticated: false,
    },
};

export const store = configureStore({
    reducer: {
        userAuthentication: authenticationSlice,
    },
    preloadedState,
});

store.subscribe(() => {
    saveState(store.getState().userAuthentication);
});
