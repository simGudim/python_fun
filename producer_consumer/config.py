import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'




#  <!-- <script>
#         $(document).ready(function(){
#             $(function() {
#                 setInterval(function() {
#                     $.ajax({
#                         type: 'GET',
#                         url: '/calculate_result',
#                         dataType : "json",
#                         success: (res) => {
#                             $('#msg_num').html(res.msg_num);
#                             $('#time').html(res.avg_time);
#                         },
#                         error: (e) => {
#                             console.log(e);
#                         }
#                     })   
#                     $.getJSON( '/calculate_result', function( data ) { 
#                         console.log(data); 
#                         });
#                 }, 1000);
#             });
#         });
#     </script> -->




