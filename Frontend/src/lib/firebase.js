import { getApps } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getDatabase } from 'firebase/database';
import { firebaseConfig } from '@/config/firebase';
import { app } from './firebaseInit';

// Only initialize auth and database on client side
export const auth = typeof window !== 'undefined' && app ? getAuth(app) : null;
export const database = typeof window !== 'undefined' && app ? getDatabase(app) : null;

export default app;
