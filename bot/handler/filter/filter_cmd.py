from aiogram.types import Message, InputFile
from scrap.analysis.filters import load_ads_data, filter_ads, filter_by_price, filter_by_location
from scrap.analysis.statistics import get_summary_statistics
from scrap.analysis.charts import create_price_histogram, create_brand_chart, create_location_chart, create_summary_chart, plot_price_histogram, plot_location_histogram
from aiogram.types import BufferedInputFile
from scrap.jobs.statistic import get_attribute_value

async def filter_cmd(message: Message):
    """
    Commande: /filter [filtres]
    Exemples :
      /filter city=Paris
      /filter min=10000 max=20000
      /filter brand=Renault city=Lyon
      /filter min=5000 max=15000 city=Marseille brand=Peugeot
      /filter city="New York" brand="Land Rover"
    """
    if not message.text:
        await message.reply("Usage: /filter [filtres]\nExemples: /filter city=Paris | /filter min=10000 max=20000 | /filter brand=\"Land Rover\" city=\"New York\"")
        return
    try:
        # Parser la commande en gérant les guillemets pour les noms avec espaces
        command_text = message.text
        parts = []
        current_part = ""
        in_quotes = False
        
        # Parser caractère par caractère pour gérer les guillemets
        for char in command_text:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current_part.strip():
                    parts.append(current_part.strip())
                current_part = ""
            else:
                current_part += char
        
        # Ajouter la dernière partie
        if current_part.strip():
            parts.append(current_part.strip())
        
        if len(parts) < 2:
            await message.reply("Usage: /filter [filtres]\nExemples: /filter city=Paris | /filter min=10000 max=20000 | /filter brand=\"Land Rover\" city=\"New York\"")
            return
        
        # Parsing flexible des arguments
        min_price = None
        max_price = None
        city = None
        brand = None
        # Pour compatibilité, on stocke les mots isolés
        keywords = []
        
        for arg in parts[1:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                key = key.lower()
                # Nettoyer les guillemets autour de la valeur
                value = value.strip().strip('"')
                if key == 'min':
                    try:
                        min_price = float(value)
                    except ValueError:
                        await message.reply(f"❌ min doit être un nombre valide")
                        return
                elif key == 'max':
                    try:
                        max_price = float(value)
                    except ValueError:
                        await message.reply(f"❌ max doit être un nombre valide")
                        return
                elif key == 'city':
                    city = value
                elif key == 'brand':
                    brand = value
                else:
                    keywords.append(value)
            else:
                # Ancien format : si nombre, c'est min/max, sinon ville
                # Nettoyer les guillemets
                clean_arg = arg.strip('"')
                try:
                    val = float(clean_arg)
                    if min_price is None:
                        min_price = val
                    elif max_price is None:
                        max_price = val
                except ValueError:
                    if city is None:
                        city = clean_arg
                    else:
                        keywords.append(clean_arg)
        
        # Charge et filtre les données
        ads = load_ads_data()
        if not ads:
            await message.reply("❌ Aucune donnée disponible. Lancez d'abord /search")
            return
        
        # Application des filtres combinés
        filtered_ads = ads
        if min_price is not None or max_price is not None:
            filtered_ads = filter_by_price(filtered_ads, min_price, max_price)
        if city:
            filtered_ads = filter_by_location(filtered_ads, [city])
        if brand:
            # Filtre par marque (attribut brand) - plus flexible pour les noms avec espaces
            brand_lower = brand.lower()
            filtered_ads = [ad for ad in filtered_ads if any(
                brand_lower in str(b).lower() or str(b).lower() in brand_lower
                for b in (get_attribute_value(ad, "brand") or [])
            )]
        # On pourrait ajouter d'autres filtres ici (keywords, etc)
        
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
        if city:
            result_msg += f"📍 Ville: {city}\n"
        if brand:
            result_msg += f"🏷 Marque: {brand}\n"
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