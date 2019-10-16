#include <iostream>
#include <random>

#include "GameClientBattlecity.h"
#include "BattlecityBlocks.h"
#include "Point.h"


void main()
{
	srand(time(0));
	GameClientBattlecity *gcb = new GameClientBattlecity("http://dojorena.io/codenjoy-contest/board/player/0?code=000000000000&gameName=battlecity");
	
	gcb->Run([&]()
	{
		bool done = false;

		gcb->Right(FireAction::AfterTurn);
		done = true;

		if (done == false)
			gcb->Blank();

	});

	getchar();
}
