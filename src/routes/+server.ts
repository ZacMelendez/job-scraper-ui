import { updateFavorites } from '../helpers/UserDatabase';
import { userStore } from './store';

import { json } from '@sveltejs/kit';

export async function POST({ request, cookies }) {
	const { user_id, favorites } = await request.json();

	console.log(user_id, favorites);

	await updateFavorites({ user_id, favorites });

	return json({ test: 'test' }, { status: 201 });
}
