
module.exports = function(app) 
{
	// application ==============================================
	app.get('*', function(req, res) {
		res.sendfile('./app/view/index.html'); 
	});
};