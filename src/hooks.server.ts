import { SvelteKitAuth } from '@auth/sveltekit';
import GoogleProvider from '@auth/core/providers/google';
import { SECRET_GOOGLE_CLIENT_ID, SECRET_GOOGLE_CLIENT_SECRET, SECRET } from '$env/static/private';
import type { Provider } from '@auth/core/providers';
import { getUser, newUser } from './helpers/UserDatabase';
import type { UserProps } from './types';

const googleProvider = GoogleProvider({
	clientId: SECRET_GOOGLE_CLIENT_ID,
	clientSecret: SECRET_GOOGLE_CLIENT_SECRET
}) as Provider;

export const handle = SvelteKitAuth({
	providers: [googleProvider],
	secret: SECRET,
	trustHost: true,
	callbacks: {
		signIn: async (params) => {
			if (!params.user) return false;

			const user = await getUser({ user_id: params.user.id });

			if (!user) {
				const newUserItem: UserProps = {
					user_id: params.user.id || '',
					name: params.user.name || '',
					email: params.user.email || '',
					image: params.user.image || '',
					favorites: []
				};

				await newUser(newUserItem);
			}

			return true;
		},
		session: async ({ session, token }) => {
			const user = await getUser({ user_id: token?.sub || '' });

			if (!user) {
				session.user = { ...session.user, id: token?.sub || '', favorites: [] };
			} else {
				session.user = {
					...session.user,
					id: token?.sub || '',
					favorites: (user.favorites as string).split(',')
				};
			}

			return session;
		}
	}
});
