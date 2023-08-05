<p align="center">
    <a href="https://bit.ly/moexx"><img src="https://bit.ly/moex_logo" alt="MOEX"></a>
</p>
<p align="center">
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/v/moex.svg?style=flat-square&logo=appveyor" alt="Version"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/l/moex.svg?style=flat-square&logo=appveyor&color=blueviolet" alt="License"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/pyversions/moex.svg?style=flat-square&logo=appveyor" alt="Python"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/status/moex.svg?style=flat-square&logo=appveyor" alt="Status"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/format/moex.svg?style=flat-square&logo=appveyor&color=yellow" alt="Format"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/wheel/moex.svg?style=flat-square&logo=appveyor&color=red" alt="Wheel"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/bitbucket/pipelines/deploy-me/moex/master?style=flat-square&logo=appveyor" alt="Build"></a>
    <a href="https://pypi.org/project/moex"><img src="https://bit.ly/moex_cov" alt="Coverage"></a>
    <a href="https://pepy.tech/project/moex"><img src="https://static.pepy.tech/personalized-badge/moex?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
    <br><br><br>
</p>

# MOEX

A little bit complex and more powerful implementation for [ISS Queries](https://bit.ly/iss_ref). See more in [documentation](https://deploy-me.bitbucket.io/moex/index.html)

## INSTALL

```bash
pip install moex
```

## USAGE

```python
import asyncio
import aiohttp
from moex import AIOMoex


async def main(aio_moex, engine="stock", market="shares", board="TQBR"):
    async with aiohttp.ClientSession() as session:
        await aio_moex.load(session=session, output_format=".json")

        # aio_moex.show_templates()

        for tmpl in aio_moex.find_template("/candles"):
            print(f"Template: {tmpl.id}. Path: {tmpl.path}")
            await aio_moex.show_template_doc(session, tmpl.id)

        df_sngsp = (
            await aio_moex.execute(
                session=session,
                url=aio_moex.render_url(
                    46,
                    engine=engine,
                    market=market,
                    security="SNGSP",
                    board=board
                    ),
                **{
                    "from": "2022-02-24",
                    "till": "2022-10-24",
                    "interval": "60"
                    }
                )
            ).to_df()
        df_yndx = (
            await aio_moex.execute(
                session=session,
                url=aio_moex.render_url(
                    155,
                    engine=engine,
                    market=market,
                    security="YNDX"
                    ),
                till="2022-01-01"
                )
            ).to_df()

        for df in (df_sngsp, df_yndx):
            print(df)     


aio_moex = AIOMoex()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(aio_moex))
```
