import { updateFavorites } from '../helpers/UserDatabase';

import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	const { user_id, favorites } = await request.json();

	console.log(user_id, favorites);

	await updateFavorites({ user_id, favorites });

	return json({ test: 'test' }, { status: 201 });
}
