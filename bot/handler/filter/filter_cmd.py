from aiogram.types import Message, InputFile
from scrap.analysis.filters import load_ads_data, filter_ads
from scrap.analysis.statistics import get_summary_statistics
from scrap.analysis.charts import create_price_histogram, create_brand_chart, create_location_chart, create_summary_chart, plot_price_histogram, plot_location_histogram
from aiogram.types import BufferedInputFile

async def filter_cmd(message: Message):
    """
    Commande: /filter [prix_min] [prix_max] [localisation]
    Exemple: /filter 10000 20000 Paris
    """
    if not message.text:
        await message.reply("Usage: /filter [prix_min] [prix_max] [localisation]\nExemple: /filter 10000 20000 Paris")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("Usage: /filter [prix_min] [prix_max] [localisation]")
            return
        
        min_price = None
        max_price = None
        location_keywords = None
        
        # Parse les arguments
        if len(parts) >= 3:
            try:
                min_price = float(parts[1])
                max_price = float(parts[2])
            except ValueError:
                await message.reply("❌ Les prix doivent être des nombres valides")
                return
        
        if len(parts) >= 4:
            location_keywords = parts[3:]
        
        # Charge et filtre les données
        ads = load_ads_data()
        if not ads:
            await message.reply("❌ Aucune donnée disponible. Lancez d'abord /search")
            return
        
        filtered_ads = filter_ads(ads, min_price, max_price, location_keywords)
        
        if not filtered_ads:
            await message.reply("❌ Aucune annonce trouvée avec ces critères")
            return
        
        # Affiche le résultat
        result_msg = f"🔍 <b>Résultats du filtrage</b>\n\n"
        result_msg += f"📦 {len(filtered_ads)} annonces trouvées\n"
        
        if min_price is not None or max_price is not None:
            price_range = ""
            if min_price is not None:
                price_range += f"Prix ≥ {min_price}€"
            if max_price is not None:
                if price_range:
                    price_range += " et "
                price_range += f"Prix ≤ {max_price}€"
            result_msg += f"💰 {price_range}\n"
        
        if location_keywords:
            result_msg += f"📍 Localisation: {' '.join(location_keywords)}\n"
        
        await message.reply(result_msg, parse_mode="HTML")
        
    except Exception as e:
        await message.reply(f"❌ Erreur lors du filtrage: {str(e)}")

async def stats_cmd(message: Message):
    """
    Commande: /stats - Affiche les statistiques générales
    """
    try:
        stats = get_summary_statistics()
        
        if stats["total_ads"] == 0:
            await message.reply("❌ Aucune donnée disponible. Lancez d'abord /search")
            return
        
        msg = "📊 <b>Statistiques générales</b>\n\n"
        msg += f"📦 Total annonces: {stats['total_ads']}\n\n"
        
        if stats["price_stats"]["count"] > 0:
            price_stats = stats["price_stats"]
            msg += "💰 <b>Statistiques des prix</b>\n"
            msg += f"   Min: {price_stats['min']:.0f}€\n"
            msg += f"   Max: {price_stats['max']:.0f}€\n"
            msg += f"   Moyenne: {price_stats['mean']:.0f}€\n"
            msg += f"   Médiane: {price_stats['median']:.0f}€\n\n"
        
        if stats["brand_stats"]:
            msg += "🏷 <b>Top 5 marques</b>\n"
            for i, (brand, count) in enumerate(list(stats["brand_stats"].items())[:5]):
                msg += f"   {i+1}. {brand}: {count} annonces\n"
        
        await message.reply(msg, parse_mode="HTML")
        
    except Exception as e:
        await message.reply(f"❌ Erreur lors du calcul des statistiques: {str(e)}")

async def chart_cmd(message: Message):
    """
    Commande: /chart [type] - Affiche un graphique
    Types: price, brand, location, summary
    """
    if not message.text:
        await message.reply("Usage: /chart [type]\nTypes: price, brand, location, summary")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("Usage: /chart [type]\nTypes: price, brand, location, summary")
            return
        
        chart_type = parts[1].lower()
        ads = load_ads_data()
        
        if not ads:
            await message.reply("❌ Aucune donnée disponible. Lancez d'abord /search")
            return
        
        if chart_type == "price":
            chart = create_price_histogram(ads)
        elif chart_type == "brand":
            chart = create_brand_chart(ads)
        elif chart_type == "location":
            chart = create_location_chart(ads)
        elif chart_type == "summary":
            chart = create_summary_chart()
        else:
            await message.reply("❌ Type de graphique invalide. Types disponibles: price, brand, location, summary")
            return
        
        await message.reply(chart, parse_mode="HTML")
        
    except Exception as e:
        await message.reply(f"❌ Erreur lors de la création du graphique: {str(e)}")

async def chart_img_cmd(message: Message):
    """
    Commande: /chartimg [type] - Envoie un graphique en image
    Types: price, ville
    """
    if not message.text:
        await message.reply("Usage: /chartimg [type]\nTypes: price, ville")
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("Usage: /chartimg [type]\nTypes: price, ville")
            return
        
        chart_type = parts[1].lower()
        ads = load_ads_data()
        
        if not ads:
            await message.reply("❌ Aucune donnée disponible. Lancez d'abord /search")
            return
        
        if chart_type == "price":
            buf = plot_price_histogram(ads)
            if buf is None:
                await message.reply("❌ Aucune annonce avec prix valide à afficher.")
                return
            caption = "Histogramme des prix"
        elif chart_type == "ville":
            buf = plot_location_histogram(ads)
            if buf is None:
                await message.reply("❌ Aucune donnée de localisation disponible.")
                return
            caption = "Top 10 des villes"
        else:
            await message.reply("❌ Type de graphique invalide. Types disponibles: price, ville")
            return
        
        buf.seek(0)
        photo = BufferedInputFile(buf.read(), filename=f"chart_{chart_type}.png")
        await message.answer_photo(photo, caption=caption)
    except Exception as e:
        await message.reply(f"❌ Erreur lors de la génération du graphique: {str(e)}") 