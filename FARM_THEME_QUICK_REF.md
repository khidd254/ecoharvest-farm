# 🌾 EcoHarvest Farm Theme - Quick Reference

## Quick Customization Guide

### Change Farm Name
**File**: `frontend/app.js` (Line ~538)
```javascript
<h1 className="text-4xl font-bold text-white mb-2">
    EcoHarvest Farm  // ← Change this
</h1>
```

### Change Tagline
**File**: `frontend/app.js` (Line ~542)
```javascript
Sustainable Farming Consultation Services  // ← Change this
```

### Change Colors
**File**: `frontend/index.html` (CSS section)
```css
/* Main background */
background: linear-gradient(135deg, #1a5f3f 0%, #2d8659 50%, #3ba86f 100%);
/* Change these hex codes to your colors */

/* Button gradient */
background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
/* Change these hex codes */
```

### Change Emojis
**File**: `frontend/app.js` (Search and replace)
- 🌾 → Your emoji
- 🌱 → Your emoji
- 🚜 → Your emoji
- 🌍 → Your emoji
- ♻️ → Your emoji

### Change Business Hours
**File**: `services.py` (Lines ~20-25)
```python
BUSINESS_START = time(8, 0)   # Change to your start time
BUSINESS_END = time(18, 0)    # Change to your end time
LUNCH_START = time(12, 0)     # Change to your lunch start
LUNCH_END = time(13, 0)       # Change to your lunch end
```

---

## Color Palette Reference

```
Forest Green:  #1a5f3f  (Dark background)
Eco Green:     #22c55e  (Buttons, accents)
Sage Green:    #16a34a  (Secondary)
Light Green:   #3ba86f  (Light backgrounds)
White:         #ffffff  (Text)
Gray:          #6b7280  (Secondary text)
Red:           #ef4444  (Errors)
Green:         #10b981  (Success)
```

---

## Emoji Quick Reference

| Emoji | Usage |
|-------|-------|
| 🌾 | Main farm icon |
| 🌱 | Seedling/growth |
| 🚜 | Tractor/farming |
| 🌍 | Earth/sustainability |
| ♻️ | Recycling |
| 👤 | User/person |
| 📧 | Email |
| 📱 | Phone |
| 📅 | Calendar/date |
| ⏰ | Time/clock |
| 📝 | Notes |
| 🔔 | Notifications |
| ✅ | Confirmed |
| ⏳ | Loading/pending |
| 📍 | Location |

---

## CSS Classes Reference

```css
.farm-gradient      /* Forest green gradient */
.eco-gradient       /* Eco-green gradient */
.gradient-text      /* Green gradient text */
.farm-icon          /* Animated sway */
.header-farm        /* Header styling */
.farm-card          /* Card with green border */
.eco-badge          /* Green badge */
.harvest-button     /* Green button */
.farm-divider       /* Green divider line */
```

---

## Key Files

| File | Purpose | Changes |
|------|---------|---------|
| `frontend/index.html` | HTML & CSS | Colors, animations, classes |
| `frontend/app.js` | React components | Branding, emojis, messaging |
| `services.py` | Business logic | Business hours (optional) |

---

## Common Customizations

### Add Custom Logo
Replace 🌾 emoji with your logo URL:
```javascript
<img src="your-logo.png" alt="Farm Logo" className="w-12 h-12" />
```

### Change Button Color
Edit `frontend/index.html`:
```css
.harvest-button {
    background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
}
```

### Add Custom Font
Add to `frontend/index.html` `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=YourFont" rel="stylesheet">
```

### Change Background Pattern
Edit `frontend/index.html` CSS:
```css
body::before {
    background-image: /* Your custom pattern */;
}
```

---

## Testing Checklist

- [ ] Farm name displays correctly
- [ ] Colors look good
- [ ] Emojis render properly
- [ ] Buttons work
- [ ] Forms submit
- [ ] Calendar displays
- [ ] Mobile responsive
- [ ] No console errors

---

## Browser Support

✅ Chrome (Latest)
✅ Firefox (Latest)
✅ Safari (Latest)
✅ Edge (Latest)
✅ Mobile browsers

---

## Performance Tips

- Keep emoji count reasonable
- Use CSS gradients (lightweight)
- Minimize custom fonts
- Test on mobile devices
- Monitor load times

---

## Troubleshooting

### Emojis not showing?
- Check browser compatibility
- Try different emoji
- Use fallback text

### Colors not right?
- Check hex codes
- Clear browser cache
- Try different browser

### Layout broken?
- Check responsive breakpoints
- Test on different screen sizes
- Review CSS changes

---

## Quick Links

- 📖 [Full Theme Guide](FARM_THEME_GUIDE.md)
- 🎨 [Visual Preview](FARM_THEME_PREVIEW.md)
- 📊 [Implementation Summary](FARM_THEME_SUMMARY.md)
- 📚 [README](README.md)

---

## Version Info

- **Theme Version**: 1.0.0
- **Status**: Production Ready
- **Last Updated**: January 2024
- **Compatibility**: 100% Backward Compatible

---

**Happy Farming! 🌾**
