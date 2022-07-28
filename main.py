import asyncio
import aiofiles
import aiohttp
from aiocsv import AsyncWriter
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


async def collect_data(city_code='2398'):
    global card_old_price, card_title, card_discoun_percentage, card_new_price
    # cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    ua = UserAgent()

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }

    async with aiohttp.ClientSession() as session:

        response = await session.get(url='https://www.atbmarket.com/ru/promo/akciya-ekonomiya?city_id=19',
                                     headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')

        cards = soup.find_all('div', class_='one-action-item')
        data = []
        for card in cards:
            try:
                card_title = card.find('div', class_="one-action-tit").text.strip()
            except:
                pass

            try:
                card_discount_percentage = card.find('div', class_='one-action-sale-perc').text.strip()
            except:
                card_discount_percentage = "No data!"
                pass

            try:
                card_old_price = card.find('div', class_='one-action-was-price').text.strip()
            except:
                card_old_price = "No data!"

                pass

            card_new_price = card.find('div', class_='one-action-price-now').text.strip().replace(' ', '.')

            data.append([card_title, card_discount_percentage, card_old_price, card_new_price])

    async with aiofiles.open(f'Parsing data.csv', 'w') as file:
        writer = AsyncWriter(file)

        await writer.writerow(
            [
                'Продукт ',
                'Процент скидки ',
                'Старая цена ',
                'Новая цена ',

            ]
        )
        await writer.writerows(data)

    print(f'Файл Parsing data.csv успешно записан!')
    return f'Parsing data.csv'


async def main():
    await collect_data()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    # asyncio.run(main())
