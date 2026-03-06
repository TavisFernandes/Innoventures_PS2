import { getApps } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getDatabase } from 'firebase/database';
import { firebaseConfig } from '@/config/firebase';
import { app } from './firebaseInit';

export const auth = getAuth(app);
export const database = getDatabase(app);

export default app;
