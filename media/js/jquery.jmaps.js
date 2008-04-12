(function($){
	// Create global object to store jmap in
	$.jmap = $.jmap || {};

	// Create object containing project details
	$.jmap.JDetails = {
		version: "2.0b",
		releaseDate: "03/03/2008",
		author: "Tane Piper <digitalspaghetti@gmail.com>",
		blog: "http://digitalspaghetti.me.uk",
		repository: "http://hg.digitalspaghetti.me.uk/jmaps",
		googleGroup: "http://groups.google.com/group/jmaps",
		licenceType: "MIT",
		licenceURL: "http://www.opensource.org/licenses/mit-license.php"
	};
	
	// Create object of errors, allows for i18n.
	$.jmap.JErrors = {
		en : {
			addressNotFound: "This address cannot be found.  Please modify your search.",
			browserNotCompatible: "This browser is reported as being not compatible with Google Maps.",
			cannotLoad: "Cannot load the Google Maps API at this time.  Please check your connection."
		},
		fr : {
			addressNotFound: "Cette adresse ne peut pas Ãªtre trouvÃ©e. Veuillez modifier votre recherche.",
			browserNotCompatible: "Ce navigateur est rapportÃ© en tant qu'Ã©tant non compatible avec des cartes de Google.",
			cannotLoad: "Ne peut pas charger les cartes api de Google actuellement. Veuillez vÃ©rifier votre raccordement."
		},
		de : {
			addressNotFound: "Diese Adresse kann nicht gefunden werden. Ã„ndern Sie bitte Ihre Suche.",
			browserNotCompatible: "Diese Datenbanksuchroutine wird als seiend nicht kompatibel mit Google Diagrammen berichtet.",
			cannotLoad: "Kann nicht die Google Diagramme API diesmal laden. ÃœberprÃ¼fen Sie bitte Ihren AnschluÃŸ."
		},
		nl : {
			addressNotFound: "Dit adres kan worden gevonden niet. Gelieve te wijzigen uw onderzoek.",
			browserNotCompatible: "Dit browser wordt gemeld zoals zijnd niet compatibel met Kaarten Google.",
			cannotLoad: "Kan de Google Kaarten API op dit moment laden niet. Gelieve te controleren uw verbinding."
		},
		es : {
			addressNotFound: "Esta direcciÃ³n no puede ser encontrada. Modifique por favor su bÃºsqueda.",
			browserNotCompatible: "Este browser se divulga como siendo no compatible con los mapas de Google.",
			cannotLoad: "No puede cargar los mapas API de Google en este tiempo. Compruebe por favor su conexiÃ³n."
		},
		sv : {
			addressNotFound: "Denna adress kunde ej hittas. Var god justera din sÃ¶kning",
			browserNotCompatible: "Denna webblÃ¤sare Ã¤r ej kompatibel med Google Maps",
			cannotLoad: "Kan inte ladda Google Maps API fÃ¶r tillfÃ¤llet. Var god kontrollera din anslutning."
		}
	};
	
	/**
	 *	jMaps Default Options
	 **/
	$.jmap.JDefaults = {
		// Initial type of map to display
		language: "en",
		// Options: "map", "sat", "hybrid"
		mapType: "map",
		// Initial map center
		mapCenter: [55.958858,-3.162302],
		// Initial map size
		mapDimensions: [400, 400],
		// Initial zoom level
		mapZoom: 12,
		// Initial map control size
		// Options: "large", "small", "none"
		mapControlSize: "small",
		// Initialise type of map control
		mapEnableType: false,
		// Initialise small map overview
		mapEnableOverview: false,
		// Enable map dragging when left button held down
		mapEnableDragging: true,
		// Enable map info windows
		mapEnableInfoWindows: true,
		// Enable double click zooming
		mapEnableDoubleClickZoom: false,
		// Enable zooming with scroll wheel
		mapEnableScrollZoom: false,
		// Enable smooth zoom
		mapEnableSmoothZoom: false,
		// Enable Google Bar
		mapEnableGoogleBar: false,
		//Debug Mode
		debugMode: false
	}
	
	$.jmap.JAdsManagerDefaults = {
		// Google Adsense publisher ID
		publisherId: ""
	};
	
	$.jmap.JFeedDefaults = {
		// URL of the feed to pass (required)
		feedUrl: "",
		// Position to center the map on (optional)
		mapCenter: []
	}
	
	$.jmap.JGroundOverlayDefauts = {
		// South West Boundry
		overlaySouthWestBounds: [],
		// North East Boundry
		overlayNorthEastBounds: [],
		// Image
		overlayImage: ""
	}
	
	$.jmap.JIconDefaults = {
		iconImage: "",
		iconShadow: "",
		iconSize: null,
		iconShadowSize: null,
		iconAnchor: null,
		iconInfoWindowAnchor: null,
		iconPrintImage: "",
		iconMozPrintImage: "",
		iconPrintShadow: "",
		iconTransparent: ""
	};
	
	// Marker manager default options
	$.jmap.JMarkerManagerDefaults = {
		// Border Padding in pixels
		borderPadding: 100,
		// Max zoom level 
		maxZoom: 17,
		// Track markers
		trackMarkers: false
	};
	
	// Default options for a point to be created
	$.jmap.JMarkerDefaults = {
		// Point lat & lng
		pointLatLng: [],
		// Point HTML for infoWindow
		pointHTML: null,
		// Event to open infoWindow (click, dblclick, mouseover, etc)
		pointOpenHTMLEvent: "click",
		// Point is draggable?
		pointIsDraggable: false,
		// Point is removable?
		pointIsRemovable: false,
		// Event to remove on (click, dblclick, mouseover, etc)
		pointRemoveEvent: "dblclick",
		// These two are only required if adding to the marker manager
		pointMinZoom: 4,
		pointMaxZoom: 17,
		// Optional Icon to pass in (not yet implemented)
		pointIcon: null,
		// For maximizing infoWindows (not yet implemented)
		pointMaxContent: null,
		pointMaxTitle: null
	};
	
	// Defaults for a Polygon
	$.jmap.JPolygonDefaults = {
		// An array of GLatLng objects
		polygonPoints: [],
		// The outer stroke colour
	 	polygonStrokeColor: "#000000",
	 	// Stroke thickness
	 	polygonStrokeWeight: 5,
	 	// Stroke Opacity
	 	polygonStrokeOpacity: 1,
	 	// Fill colour
	 	polygonFillColor: "#ff0000",
	 	// Fill opacity
	 	polygonFillOpacity: 1,
	 	// Optional center map
	 	mapCenter: [],
	 	// Is polygon clickable?
	 	polygonClickable: true
	};
	
	// Default options for a Polyline
	$.jmap.JPolylineDefaults = {
		// An array of GLatLng objects
		polylinePoints: [],
		// Colour of the line
		polylineStrokeColor: "#ff0000",
		// Width of the line
		polylineStrokeWidth: 10,
		// Opacity of the line
		polylineStrokeOpacity: 1,
		// Optional center map
		mapCenter: [],
		// Is line Geodesic (i.e. bends to the curve of the earth)?
		polylineGeodesic: false,
		// Is line clickable?
		polylineClickable: true
	};
	
	$.jmap.JSearchAddressDefaults = {
		// Address to search for
		address: null,
		// Option to add marker for address
		addMarker: false,
		// Show address in infoWindow of point is added
		showAddress: false,
		// Optional Cache to store Geocode Data (not implemented yet)
		cache: {},
		// Country code for localisation (not implemented yet)
		countryCode: 'uk'
	};
	
	$.jmap.JSearchDirectionsDefault = {
		// From address
		fromAddress: "",
		// To address
		toAddress: "",
		// Optional panel to show text directions
		directionsPanel: ""
	};
	
	$.jmap.JTrafficDefaults = {
		// Can pass in "create" (default) or "destroy" which will remove the layer
		method: "create",
		// Center the map on this point (optional)
		mapCenter: []
	};
	
	$.jmap.JMoveToDefaults = {
		centerMethod: 'normal',
		mapType: null,
		mapCenter: [],
		mapZoom: null
	}
	
	$.jmap.JSavePositionDefaults = {
		recall: false
	}
	
})(jQuery);

(function($) {
	/**
	 *	This is the core function called from the .jmap() alias that creates
	 *	the Google map and jQuery object.
 	 *	@param jQuery el (required) A jQuery object containing the target element for the map
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@cat jMapCore
	 *	@name jmap
	 */
	$.jmap.init = function(el, options, callback) {
	
		/* Set Up Options */
		// First we create out options object by checking passed options
		// and that no defaults have been overidden
		var options = $.extend({}, $.jmap.JDefaults, options);
		// Check for metadata plugin support
		var options = $.jmap.JOptions = $.meta ? $.extend({}, options, $(this).data()) : options;
		/* End Set Up Options */
		
		// Do checks or throw errors
		$.jmap._initChecks(el);
		
		// Initialise the GMap2 object
		el.jmap = $.jmap.GMap2 = new GMap2(el);
		// Set map type based on passed option
		var mapType = $.jmap._initMapType(options.mapType);
		
		// Initialise the map with the passed settings
		el.jmap.setCenter(new GLatLng(options.mapCenter[0], options.mapCenter[1]), options.mapZoom, mapType);
			
		// Attach a controller to the map view
		// Will attach a large or small.  If any other value passed (i.e. "none") it is ignored
		switch(options.mapControlSize)
		{
			case "small":
				el.jmap.addControl(new GSmallMapControl());
			break;
			case "large":
				el.jmap.addControl(new GLargeMapControl());
			break;
		}
		// Type of map Control (Map,Sat,Hyb)
		if(options.mapEnableType)
			el.jmap.addControl(new GMapTypeControl()); // Off by default
		
		// Show the small overview map
		if(options.mapEnableOverview)
			el.jmap.addControl(new GOverviewMapControl());// Off by default
		
		// GMap2 Functions (in order of the docs for clarity)
		// Enable a mouse-dragable map
		if(!options.mapEnableDragging)
			el.jmap.disableDragging(); // On by default
			
		// Enable Info Windows
		if(!options.mapEnableInfoWindows)
			el.jmap.disableInfoWindow(); // On by default
		
		// Enable double click zoom on the map
		if(options.mapEnableDoubleClickZoom)
			el.jmap.enableDoubleClickZoom(); // On by default
		
		// Enable scrollwheel on the map
		if(options.mapEnableScrollZoom)
			el.jmap.enableScrollWheelZoom(); //Off by default
		
		// Enable smooth zooming
		if (options.mapEnableSmoothZoom)
			el.jmap.enableContinuousZoom(); // Off by default

		// Enable Google Bar
		if (options.mapEnableGoogleBar)
			el.jmap.enableGoogleBar();  //Off by default

		// output init to console
		if (options.debugMode) {
		    console.log(el.jmap);
		}
		
		if (typeof callback == 'function') return callback();
	}
	
	/**
	 *	.addFeed(options, callback?);
	 *	This function takes a KML or GeoRSS file and
	 *	adds it to the map
	 */
	$.jmap.addFeed = function(options, callback) {
	
		var options = $.extend({}, $.jmap.JFeedDefaults, options);
		
		// Load feed
		var feed = new GGeoXml(options.feedUrl);
		// Add as overlay
		$.jmap.GMap2.addOverlay(feed);
		
		// If the user has passed the optional mapCenter,
		// then center the map on that point
		if (options.mapCenter[0] && options.mapCenter[1])
			$.jmap.GMap2.setCenter(new GLatLng(options.mapCenter[0], options.mapCenter[1]));
		
		if (typeof callback == 'function') return callback();
	}
	
	$.jmap.addGroundOverlay = function(options, callback) {
		var options = $.extend({}, $.jmap.JGroundOverlayDefaults, options);
		var boundries = new GLatLngBounds(new GLatLng(options.overlaySouthWestBounds[0], options.overlaySouthWestBounds[1]), new GLatLng(options.overlayNorthEastBounds[0], options.overlayNorthEastBounds[1]));
		
		$.jmap.GGroundOverlay = new GGroundOverlay(options.overlayImage, boundries);
		$.jmap.GMap2.addOverlay($.jmap.GGroundOverlay);
		
		if (typeof callback == 'function') return callback();
	}
	
	/**
	 *	Create a marker and add it as a point to the map
	 */
	$.jmap.addMarker = function(options, callback) {
		// Create options
		var options = $.extend({}, $.jmap.JMarkerDefaults, options);
		var markerOptions = {}
		
		if (typeof options.pointIcon == 'object')
			$.extend(markerOptions, {icon: options.pointIcon});
		
		if (options.pointIsDraggable)
			$.extend(markerOptions, {draggable: options.pointIsDraggable});
		
		// Create marker, optional parameter to make it draggable
		var marker = new GMarker(new GLatLng(options.pointLatLng[0],options.pointLatLng[1]), markerOptions);
		
		// If it has HTML to pass in, add an event listner for a click
		if(options.pointHTML)
			GEvent.addListener(marker, options.pointOpenHTMLEvent, function(){
				marker.openInfoWindowHtml(options.pointHTML, {maxContent: options.pointMaxContent, maxTitle: options.pointMaxTitle});
			});

		// If it is removable, add dblclick event
		if(options.pointIsRemovable)
			GEvent.addListener(marker, options.pointRemoveEvent, function(){
				$.jmap.GMap2.removeOverlay(marker);
			});

		// If the marker manager exists, add it
		if($.jmap.GMarkerManager) {
			$.jmap.GMarkerManager.addMarker(marker, options.pointMinZoom, options.pointMaxZoom);	
		} else {
			// Direct rendering to map
			$.jmap.GMap2.addOverlay(marker);
		}
		
		if (typeof callback == 'function') return callback();
	}
	
	/**
	 * Create a polygon and render to the map
	 */
	 $.jmap.addPolygon = function(options, callback) {
	 	
	 	var options = $.extend({}, $.jmap.JPolygonDefaults, options);
		polygonOptions = {};
	 	if (!options.polygonClickable)
			var polygonOptions = $.extend({}, polygonOptions, {
				clickable: false
			});
	 		
	 	if(options.mapCenter[0] && options.mapCenter[1])
	 		$.jmap.GMap2.setCenter(new GLatLng(options.mapCenter[0], options.mapCenter[1]));
		
		var polygon = new GPolygon(options.polygonPoints, options.polygonStrokeColor, options.polygonStrokeWeight, options.polygonStrokeOpacity, options.polygonFillColor, options.polygonFillOpacity, polygonOptions);

		$.jmap.GMap2.addOverlay(polygon);
		
		if (typeof callback == 'function') return callback();
	 }
	
	/**
	 *	Create a polyline and render on the map
	 */
	$.jmap.addPolyline = function (options, callback) {
		var options = $.extend({}, $.jmap.JPolylineDefaults, options);
		var polyLineOptions = {};
		if (options.polylineGeodesic)
			$.extend({}, polyLineOptions, {geodesic: true});
			
		if(!options.polylineClickable)
			$.extend({}, polyLineOptions, {clickable: false});

		if (options.mapCenter[0] && options.mapCenter[1])
			$.jmap.GMap2.setCenter(new GLatLng(options.mapCenter[0], options.mapCenter[1]));

		var polyline = new GPolyline(options.polylinePoints, options.polylineStrokeColor, options.polylineStrokeWidth, options.polylineStrokeOpacity, polyLineOptions);
		$.jmap.GMap2.addOverlay(polyline);
		
		if (typeof callback == 'function') return callback();
	}
		
	/**
	 *	.trafficInfo(options?, callback?);
	 *	This function renders a traffic info
	 *	overlay for supported cities
	 *	The GTrafficOverlay also has it's own show/hide methods
	 *	that do not destory the overlay.  Can be called:
	 *	$.jmap.GTrafficOverlay.show();
	 *	$.jmap.GTrafficOverlay.hide();
	 */
	$.jmap.addTrafficInfo = function(options, callback) {
		var options = $.extend({}, $.jmap.JTrafficDefaults, options);
		
		// Does the user wants to create or destory the overlay
		switch(options.method) {
			case "create":
				$.jmap.GTrafficOverlay = new GTrafficOverlay;
				// Add overlay
				$.jmap.GMap2.addOverlay($.jmap.GTrafficOverlay);
				// If the user has passed the optional mapCenter,
				// then center the map on that point
				if (options.mapCenter[0] && options.mapCenter[1]) {
					$.jmap.GMap2.setCenter(new GLatLng(options.mapCenter[0], options.mapCenter[1]));
				}
			break;
			case "destroy":
				// Distroy overlay
				$.jmap.GMap2.removeOverlay($.jmap.GTrafficOverlay);
			break;
		
		}
		if (typeof callback == 'function') return callback();
	}
	
	$.jmap.disableTraffic = function(callback) {
		$.jmap.GTrafficOverlay.hide();
		if (typeof callback == 'function') return callback();
	}
	
	$.jmap.enableTraffic = function(callback) {
		$.jmap.GTrafficOverlay.show();
		if (typeof callback == 'function') return callback();
	}
	
	/**
	 *	Create a AdSense ad manager
	 */
	$.jmap.createAdsManager = function(options, callback) {
		var options = $.extend({}, $.jmap.JAdsManagerDefaults, options);
	
		$.jmap.GAdsManager = new GAdsManager($.jmap.GMap2, options.publisherId);
		
		if (typeof callback == 'function') return callback();
	}
	
	$.jmap.hideAds = function(callback){
		$.jmap.GAdsManager.disable();
		if (typeof callback == 'function') return callback();
	}
	
	$.jmap.showAds = function(callback){
		$.jmap.GAdsManager.enable();
		if (typeof callback == 'function') return callback();
	}
	
	// Create Geocoder cache and attach to global object
	$.jmap.createGeoCache = function(callback) {
		$.jmap.GGeocodeCache = new GGeocodeCache();
		if (typeof callback == 'function') return callback();
	}
	
	// Create a geocoder object
	$.jmap.createGeoCoder = function(cache, callback) {
		if (cache) {
			// Create with cache
			$.jmap.GClientGeocoder = new GClientGeocoder(cache);
		} else {
			// No cache
			$.jmap.GClientGeocoder = new GClientGeocoder;
		}
		if (typeof callback == 'function') return callback();
	}
	
	/**
	 * Create an icon to return to addMarker
	 */
	$.jmap.createIcon = function(options) {
		var options = $.extend({}, $.jmap.JIconDefaults, options);
		var icon = new GIcon(G_DEFAULT_ICON);
		
		if(options.iconImage)
			icon.image = options.iconImage;
		if(options.iconShadow)
			icon.shadow = options.iconShadow;
		if(options.iconSize)
			icon.iconSize = options.iconSize;
		if(options.iconShadowSize)
			icon.shadowSize = options.iconShadowSize;
		if(options.iconAnchor)
			icon.iconAnchor = options.iconAnchor;
		if(options.iconInfoWindowAnchor)
			icon.infoWindowAnchor = options.iconInfoWindowAnchor;
	
		return icon;
	}
	
	/**
	 *	Creates the marker manager and attaches it to the $.jmap namespace
	 */
	$.jmap.createMarkerManager = function(options, callback) {
		// Merge the options with the defaults
		var options = $.extend({}, $.jmap.JMarkerManagerDefaults, options);
		// Create the marker manager and attach to the global object
		$.jmap.GMarkerManager = new GMarkerManager($.jmap.GMap2, options);
		// Return the callback
		if (typeof callback == 'function') return callback();
	}
		
	// This is an alias function that allows the user to simply search for an address
	// Can be returned as a result, or as a point on the map
	$.jmap.searchAddress = function(options, pass, callback) {
	
		var options = $.extend({}, $.jmap.JSearchAddressDefaults, options);
		
		// Add options from pass to marker object
		var pass = $.extend({}, $.jmap.JMarkerManagerDefaults, pass);
		
		// Check to see if the Geocoder already exists in the object
		// or create a temporary locally scoped one.
		if (typeof $.jmap.GClientGeocoder == 'undefined') {
			 var geocoder = new GClientGeocoder;
		} else {
			var geocoder = $.jmap.GClientGeocoder;
		}
		
		// Geocode the address
		geocoder.getLatLng(options.address, function(point){
				if (!point) {
					// Address is not found, throw an error
					throw new Error($.jmap.JErrors[$.jmap.JOptions.language].addressNotFound);
				} else {
					// Center map on point
					$.jmap.GMap2.setCenter(point);

					if (options.debugMode) {
						console.log(point.x);
						console.log(point.y);
					}

					// If user wants to add marker, get the lat/lng details
					if (options.addMarker) {
						pass.pointLatLng = [point.y, point.x];
						// Optional show address in a bubble
						if (options.showAddress)
							pass.pointHTML = options.address;
							
						// Add marker to map
						$.jmap.addMarker(pass);
					} else {
						// Return geocoded object
						return point;
					}
				}
		}, callback);	// Fire optional callback supported by the GClientGeocoder
	}
	

	/**
	 *	.searchDirections(options, callback?);
	 *	This function allows you to pass a to and from address.  If To address
	 *	is previous from address, automatically creates a GRoute object
	 */	
	$.jmap.searchDirections = function(options, callback) {	
		var options = $.extend({}, $.jmap.JSearchDirectionsDefaults, options);
		var panel = $('#' + options.directionsPanel).get(0);
		$.jmap.GDirections = new GDirections($.jmap.GMap2, panel);
		$.jmap.GDirections.load(options.fromAddress + ' to ' + options.toAddress);
		if (typeof callback == 'function') return callback();
	}
	
	$.jmap.moveTo = function(options, callback) {
		
		var options = $.extend({}, $.jmap.JMoveToDefaults, options);
		if (options.mapType)
			var mapType = $.jmap._initMapType(options.mapType);
		var point = new GLatLng(options.mapCenter[0], options.mapCenter[1]);
		switch (options.centerMethod) {
			case 'normal':
				$.jmap.GMap2.setCenter(point, options.mapZoom, mapType);
				break;
			case 'panTo':
				$.jmap.GMap2.panTo(point);
				break;
		}
		if (typeof callback == 'function') return callback();
	}
	
	$.jmap.savePosition = function(options, callback) {
		var options = $.extend({}, $.jmap.JMoveToDefaults, options);
		if (options.recall) {
			$.jmap.GMap2.returnToSavedPosition();
		} else {
			$.jmap.GMap2.savePosition();
		}
		if (typeof callback == 'function') return callback();
	}
	
	$.jmap.createKeyboardHandler = function(callback){
		$.jmap.keyboardHandler = new GKeyboardHandler($.jmap.GMap2);
		if (typeof callback == 'function') return callback();
	}

	/* Internal Functions */
	
	/**
	 *	Function: 	setMapType
	 *	Accepts: 	string maptype
	 *	Returns:	CONSTANT maptype
	 **/ 
	$.jmap._initMapType = function(option) {
		// Lets set our map type based on the options
		switch(option) {
			case "map":	// Normal Map
				var maptype = G_NORMAL_MAP;
			break;
			case "sat":	// Satallite Imagery
				var maptype = G_SATELLITE_MAP;
			break;
			case "hybrid":	//Hybrid Map
				var maptype = G_HYBRID_MAP;
			break;
		}
		return maptype;	
	}
	
	$.jmap._initChecks = function(el) {
		// Check if API can be loaded
		if (typeof GBrowserIsCompatible == 'undefined') {
			// Because map does not load, provide visual error
			$(el).text($.jmap.JErrors[$.jmap.JOptions.language].cannotLoad).css({
				color: "#f00"
			});
			// Throw exception
			throw Error($.jmap.JErrors[$.jmap.JOptions.language].cannotLoad);
		}
		// Check to see if browser is compatible, if not throw and exception
		if (!GBrowserIsCompatible()) {
			// Because map does not load, provide visual error
			$(el).text($.jmap.JErrors[$.jmap.JOptions.language].browserNotCompatible).css({color: "#f00"});
			// Throw exception
			throw Error($.jmap.JErrors[$.jmap.JOptions.language].browserNotCompatible);
		}
	}
})(jQuery);
// End of closure

(function($){
		/**
	 *	Activates the google map
	 *	@example $('#map').jmap({mapType: 'hybrid'});
	 *	@desc Activates a Google map with the Hybrid graphics settings
	 *	@example $('#map').jmap({mapType: 'hybrid'}, function(){ alert('Map Loaded'); });
	 *	@desc Activates a Google map with the Hybrid graphics settings and fires a callback
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name jmap
	 */
	$.fn.jmap = function(options, callback) {
		return this.each(function(){
			new $.jmap.init(this, options, callback);
		});
	}

	/**
	 *	Adds a KML or GeoRSS feed to the map
	 *	@example $('#map').addFeed({feed: 'http://digitalspaghetti.me.uk/my.kml', mapCenter:[55.958858,-3.162302]});
	 *	@desc Adds the KML feed to the map and displays the points.  Also centers the map on a new location.
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name addFeed
	 */
	 $.fn.addFeed = function(options, callback) {
	 	return this.each(function(){
	 		new $.jmap.addFeed(options, callback);
	 	});
	 }
	 
	 /**
	 *	Adds a ground overlay (bitmap image) over the map
	 *	@example $('#map').addGroundOverlay({sw: [55.958858,-3.162302], ne: [56.958858,-3.262302], image: "http://digitalspaghetti.me.uk/overlay.gif"});
	 *	@desc Adds a ground overlay image within the bounding box set by the the South West and North East points
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name addGroundOverlay
	 */
	 $.fn.addGroundOverlay = function(options, callback) {
	 	return this.each(function(){
	 		new $.jmap.addGroundOverlay(options, callback);
	 	});
	 }
	
	/**
	 *	Adds a marker to the map
	 *	@example $('#map').addMarker({pointLat: 55.958858, pointLng: -3.162302});
	 *	@desc Add's a basic marker to the map
	 *	@example $('#map').addMarker({pointLat: 55.958858, pointLng: -3.162302, pointHTML: "Point 1"});
	 *	@desc Add's a marker to the map with a HTML bubble (activates on click)
	 *	@example $('#map').addMarker({pointLat: 55.958858, pointLng: -3.162302, pointHTML: "Point 1", openHTMLEvent: "mouseover"});
	 *	@desc Add's a marker to the map that activates the HTML bubble with a mouseover event
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name addMarker
	 */
	$.fn.addMarker = function(options, callback) {
		return this.each(function(){
			new $.jmap.addMarker(options, callback);
		});
	}
	
	/**
	 *	Adds a polygon to the map from an array of GLatLng points
	 *	@example $('#map').addPolygon({points: [new GLatLng(55.958858,-3.162302), new GLatLng(55.968858,-3.162302), new GLatLng(55.968858,-3.152302), new GLatLng(55.958858,-3.152302), new GLatLng(55.958858,-3.162302)]});
	 *	@desc Adds a basic polygon to the map.
	 *	@example $('#map').addPolygon({points: [new GLatLng(55.958858,-3.162302), new GLatLng(55.968858,-3.162302), new GLatLng(55.968858,-3.152302), new GLatLng(55.958858,-3.152302), new GLatLng(55.958858,-3.162302)], strokeColor "#f00"});
	 *	@desc Adds a basic polygon to the map with a red stroke line.
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name addPolygon
	 */
	 $.fn.addPolygon = function(options, callback) {
	 	return this.each(function(){
	 		new $.jmap.addPolygon(options, callback);
	 	});
	 }
	
	/**
	 *	Adds a polyline to the map
	 *	@example $('#map').addPolyline({points: [new GLatLng(55.958858,-3.162302), new GLatLng(55.968858,-3.162302), new GLatLng(55.988858,-3.262302)]});
	 *	@desc Adds a polyline to the map
	 *	@example $('#map').addPolyline({points: [new GLatLng(55.958858,-3.162302), new GLatLng(55.968858,-3.162302), new GLatLng(55.988858,-3.262302)], strokeColor "#f00"});
	 *	@desc Adds a red polyline to the map	 
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name addPolyline
	 */
	$.fn.addPolyline = function(options, callback) {
	 	return this.each(function(){
	 		new $.jmap.addPolyline(options, callback);
	 	});
	 }
	
	/**
	 *	Adds a traffic info layer to the map.  There can only be one layer on the map, and this service is
	 *  not available in all localities.
	 *	@example $('#map').addTrafficInfo();
	 *	@desc Creates a traffic information layer on the map
	 *	@example $('#map').addTrafficInfo({mapCenter[55.958858,-3.162302]});
	 *	@desc Adds a layer of traffic info and centers the map
	 *	@example $('#map').addTrafficInfo({method: "destory"});
	 *	@desc Destroys the traffic layer from the map
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name addTrafficInfo
	 */
	 $.fn.addTrafficInfo = function(options, callback) {
	 	return this.each(function(){
	 		new $.jmap.addTrafficInfo(options, callback);
	 	});
	 }
	 
	/**
	 *	Hides the taffic layer without destroying it
	 *	@example $('#map').hideTraffic();
	 *	@type none
	 *	@name hideTraffic
	 */
	 $.fn.hideTraffic = function() {
	 	return this.each(function(){
	 		new $.jmap.disableTraffic();
	 	});
	 }
	 
	 /**
	 *	Shows the taffic layer thats been hidden
	 *	@example $('#map').showTraffic();
	 *	@type none
	 *	@name showTraffic
	 */
	 $.fn.showTraffic = function() {
	 	return this.each(function(){
	 		new $.jmap.enableTraffic();
	 	});
	 }
	 
	 /**
	 *	Creates a Google AdSense layer on the map
	 *  not available in all localities.
	 *	@example $('#map').createAdsManager({publisherId: "YourAdsenseKey"});
	 *	@desc Creates a ad layer on the map using your AdSense key
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name createAdsManager
	 */
	 $.fn.createAdsManager = function(options, callback) {
		return this.each(function(){
			new $.jmap.createAdsManager(options, callback);
		});
	}

	/**
	 *	Hides the ad layer
	 *	@example $('#map').hideAds();
	 *	@param Function callback (optional) An optional callback
	 *	@type none
	 *	@name hideAds
	 */
	$.fn.hideAds = function(callback) {
		return this.each(function(){
			new $.jmap.hideAds(callback);
		});
	}
	
	/**
	 *	Shows the ad layer
	 *	@example $('#map').showAds();
	 *	@param Function callback (optional) An optional callback
	 *	@type none
	 *	@name showAds
	 */
	$.fn.showAds = function(callback) {
		return this.each(function(){
			new $.jmap.showAds(callback);
		});
	}
	
	/**
	 *	Creates a Google Geocode cache to store geocoding request
	 *	@example $('#map').createGeoCache();
	 *	@desc Creates a cache to store geocode requests
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name createGeoCache
	 */
	$.fn.createGeoCache = function(callback) {
		return this.each(function(){
			new $.jmap.createGeoCache(callback);
		});
	}
	
	/**
	 *	Creates a Google Geocoding object
	 *	@example $('#map').createGeoCoder();
	 *	@desc Creates a geocoder to return Lat/Lng co-ordinates from an address.
 	 *	@param Object cache (optional) An object geocache to store the geocode request
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name createGeoCoder
	 */
	$.fn.createGeoCoder = function(cache, callback) {
		return this.each(function(){
			new $.jmap.createGeoCoder(cache);
		});
	}
	
	/**
	 *	Creates a Google marker manager
	 *	@example $('#map').createMarkerManager();
	 *	@desc Creates a marker manager to store markers
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name createMarkerManager
	 */
	$.fn.createMarkerManager = function(options, callback) {
		return this.each(function(){
			new $.jmap.createMarkerManager(options, callback);
		});
	}
	
	/**
	 *	Searches for an address and returns is as co-ordinates or as a marker
	 *	@example $('#map').searchAddress({address: "123 Test St, Edinburgh"});
	 *	@desc Passes the address to the Geocoder object and returns the Lat/Lng
	 *	@example $('#map').searchAddress({address: "123 Test St, Edinburgh", addMarker: true, showAddress: true});
	 *	@desc Passes the address to the Geocoder object and returns a marker with address in the info window
	 *	@param Object options (optional) An object containing options
	 *	@param Object pass (optional) Options to overide the marker
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name searchAddress
	 */
	$.fn.searchAddress = function(options, pass, callback) {
		return this.each(function() {
			new $.jmap.searchAddress(options, pass, callback);
		});
	}
	
	/**
	 *	Searches for directions between two or more points, and displays on the map
	 *	and within directions text area
	 *	@example $('#map').searchDirections({fromAddress: "123 Test St, Edinburgh", toAddress:"15 jQuery Rd, Edinburgh", directionsPanel:"directions"});
	 *	@desc Searches the directions between the two addresses, returns to the map and to a div with the ID of 'directions'
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name searchDirections
	 */
	$.fn.searchDirections = function(options, callback) {
		return this.each(function(){
			new $.jmap.searchDirections(options, callback);
		});
	}
	
	/**
	 *	Move to co-ordinates on the map
	 *	@example $('#map').moveTo({mapCenter: [55.958858,-3.162302]});
	 *	@desc Centers the map on the selected co-ordinates
	 *	@example $('#map').moveTo({mapCenter: [55.958858,-3.162302], centerMethod: "pan"});
	 *	@desc Pans from the current position to the selected co-ordinates
	 *	@example $('#map').moveTo({mapCenter: [55.958858,-3.162302], mapType: "map"});
	 *	@desc Centers the map on the selected co-ordinates and changes maptype to Map
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name moveTo
	 */
	$.fn.moveTo = function(options, callback) {
		return this.each(function(){
			new $.jmap.moveTo(options, callback)
		});
	}
	
	/**
	 *	Saves the current position or retrives the save position
	 *	@example $('#map').savePosition();
	 *	@desc Saves the current position
	 *	@example $('#map').savePosition({recall:true});
	 *	@desc Recalls the saved position and centers the map on it
	 *	@param Object options (optional) An object containing options
	 *	@param Function callback (optional) An optional callback
	 *	@type jQuery
	 *	@name savePosition
	 */
	$.fn.savePosition = function(options, callback) {
		return this.each(function(){
			new $.jmap.savePosition(options, callback)
		});
	}
	
	/**
	 *	Enables the map keyboard handler, which allows the map to capture keyboard events.
	 *	@example $('#map').createKeyboardHandler();
	 *	@desc Creates the keyboard handler
	 *	@param Function callback (optional) An optional callback
	 *	@type none
	 *	@name createKeyboardHandler
	 */
	$.fn.createKeyboardHandler = function(callback){
		return this.each(function(){
			new $.jmap.createKeyboardHandler(callback);
		});
	}
	
})(jQuery);