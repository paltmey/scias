/**
 * Created by philippaltmeyer on 07.05.17.
 */
r.expr([{'id':'978', 'weight':'0.95'}, {'id':'473', 'weight':'0.67'}, {'id':'976', 'weight':'1.0'}, {'id':'406', 'weight':'1.0'}, {'id':'450', 'weight':'1.0'}, {'id':'473', 'weight':'1.0'}, {'id':'538', 'weight':'1.0'}, {'id':'359', 'weight':'1.0'}, {'id':'175', 'weight':'1.0'}, {'id':'672', 'weight':'1.0'}, {'id':'392', 'weight':'1.0'}, {'id':'545', 'weight':'1.0'}])
  .eqJoin('node', r.db('vor').table('key_frame_predictions'), {index:'node'}).zip().map(function(row) {
    return {
      'key_frame_id': row('key_frame_id'),
        'weighted_score': row('weight').coerceTo('number').mul(row('score').coerceTo('number'))
    }
  }).group('key_frame_id').reduce(function(left, right) {
    return {
      'weighted_score': left('weighted_score').add(right('weighted_score'))
    }
  }).ungroup().map(function(row) {
    return {
      'key_frame_id': row('group'),
      'weighted_score_sum': row('reduction')('weighted_score')
    }
  }).orderBy(r.desc('weighted_score_sum'));


r.db('vor').table('imagenet_labels').eqJoin(r.row('node'), r.db('vor').table('key_frame_predictions'), {index:'node'}).zip().filter({'key_frame_id':'ee298661-e95c-4e45-805a-a5a17728cd3c'}).group('key_frame_id')


[{'id': '1313', 'weight': '0.383652090591'}, {'id': '1026', 'weight': '0.356556137683'}, {'id': '934', 'weight': '0.304725764541'}, {'id': '1096', 'weight': '0.345231752216'}, {'id': '1290', 'weight': '0.35397115067'}, {'id': '1805', 'weight': '0.308607327121'}, {'id': '885', 'weight': '0.34776488262'}, {'id': '1622', 'weight': '0.307486410744'}, {'id': '1399', 'weight': '0.321110314013'}, {'id': '1017', 'weight': '0.3688361175'}];


r.db('vor').table('imagenet_labels').getAll('1313', '1026', '934', '1096', '1290', '1805', '885', '1622', '1399', '1017').map(function(row){
  return {'node': row('node'), 'weight': r.expr({'1313':'0.383652090591', '1026':'0.356556137683', '934':'0.304725764541', '1096':'0.345231752216', '1290':'0.35397115067', '1805':'0.308607327121', '885':'0.34776488262', '1622':'0.307486410744','1399':'0.321110314013', '1017': '0.3688361175'})(row('id'))}
})


r.db('vor').table('key_frame_predictions').getAll('151', '4', '276', {index:'node'}).map(function(row) {
  return {
    'key_frame_id': row('key_frame_id'),
    'weighted_score': r.expr({'151':0.8031198193854081, '4':0.687724392349109, '276':0.6745881345758562})(row('node'))
.mul(row('score').coerceTo('number'))}})
.group('key_frame_id').reduce(function(left, right){
  return {'weighted_score': left('weighted_score').add(right('weighted_score'))}})
.ungroup()
.map(function(row){
  return {
    'key_frame_id': row('group'),
    'weighted_score_sum': row('reduction')('weighted_score')
  }})
.eqJoin('key_frame_id', r.db('vor').table('key_frames'))
.without({'right': 'id'})
.zip()
.orderBy(r.desc('weighted_score_sum'))
.slice(0, 10)
