<?php echo $header; ?><?php echo $column_left; ?>
<div id="content">
  <div class="page-header">
    <div class="container-fluid">
      <div class="pull-right">
        <button type="submit" form="form-jade-footer" data-toggle="tooltip" title="<?php echo $button_save; ?>" class="btn btn-primary"><i class="fa fa-save"></i></button>
        <a href="<?php echo $cancel; ?>" data-toggle="tooltip" title="<?php echo $button_cancel; ?>" class="btn btn-default"><i class="fa fa-reply"></i></a></div>
      <h1><?php echo $heading_title; ?></h1>
      <ul class="breadcrumb">
        <?php foreach ($breadcrumbs as $breadcrumb) { ?>
        <li><a href="<?php echo $breadcrumb['href']; ?>"><?php echo $breadcrumb['text']; ?></a></li>
        <?php } ?>
      </ul>
    </div>
  </div>
  <div class="container-fluid">
    <?php if ($error_warning) { ?>
    <div class="alert alert-danger"><i class="fa fa-exclamation-circle"></i> <?php echo $error_warning; ?>
      <button type="button" class="close" data-dismiss="alert">&times;</button>
    </div>
    <?php } ?>
    <?php if ($success) { ?>
    <div class="alert alert-success"><i class="fa fa-check-circle"></i> <?php echo $success; ?>
      <button type="button" class="close" data-dismiss="alert">&times;</button>
    </div>
    <?php } ?>
    <div class="panel panel-default">
      <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-pencil"></i> <?php echo $text_edit; ?></h3>
      </div>
      <div class="panel-body">
        <form action="<?php echo $action; ?>" method="post" enctype="multipart/form-data" id="form-jade-footer" class="form-horizontal">
          <ul class="nav nav-tabs">
            <li class="active"><a href="#tab-general" data-toggle="tab"><?php echo $tab_general; ?></a></li>
            <li><a href="#tab-description" data-toggle="tab"><?php echo $tab_description; ?></a></li>
            <li><a href="#tab-links" data-toggle="tab"><?php echo $tab_links; ?></a></li>
            <li><a href="#tab-colors" data-toggle="tab"><?php echo $tab_colors; ?></a></li>
          </ul>
          <div class="tab-content">
            <div class="tab-pane active" id="tab-general">
              <fieldset>
                <legend class=""><?php echo $text_control_panel; ?></legend>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_status; ?></label>
                  <div class="col-sm-3">
                    <select name="jade_footer_copyright_status" class="form-control">
                      <?php if ($jade_footer_copyright_status) { ?>
                      <option value="1" selected="selected"><?php echo $text_enabled; ?></option>
                      <option value="0"><?php echo $text_disabled; ?></option>
                      <?php } else { ?>
                      <option value="1"><?php echo $text_enabled; ?></option>
                      <option value="0" selected="selected"><?php echo $text_disabled; ?></option>
                      <?php } ?>
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_background_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_copyright_background_color" value="<?php echo $jade_footer_copyright_background_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_font_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_copyright_font_color" value="<?php echo $jade_footer_copyright_font_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
              </fieldset>
            </div>
            <div class="tab-pane" id="tab-description">
              <div class="form-group">
                <label class="col-sm-2 control-label"><?php echo $entry_description_sizeclass; ?></label>
                <div class="col-sm-10">
                  <select name="jade_footer_copyright_description_sizeclass" class="form-control">
                    <?php foreach($size_classes as $size_class_value) { ?>
                    <?php if($size_class_value['code'] == $jade_footer_copyright_description_sizeclass) { ?>
                    <option value="<?php echo $size_class_value['code']; ?>" selected="selected"><?php echo $size_class_value['title']; ?></option>
                    <?php } else { ?>
                    <option value="<?php echo $size_class_value['code']; ?>"><?php echo $size_class_value['title']; ?></option>
                    <?php } ?>
                    <?php } ?>
                  </select>
                </div>
              </div>
              <ul class="nav nav-tabs" id="editor-language">
                <?php foreach ($languages as $language) { ?>
                <li><a href="#editor-language<?php echo $language['language_id']; ?>" data-toggle="tab"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /> <?php echo $language['name']; ?></a></li>
                <?php } ?>
              </ul>
              <div class="tab-content">
                <?php foreach ($languages as $language) { ?>
                <div class="tab-pane" id="editor-language<?php echo $language['language_id']; ?>">
                  <div class="form-group required">
                    <label class="col-sm-2 control-label"><?php echo $entry_description; ?></label>
                    <div class="col-sm-10">
                      <textarea name="jade_footer_copyright_description[<?php echo $language['language_id']; ?>][description]" placeholder="<?php echo $entry_description; ?>" id="input-editor-description<?php echo $language['language_id']; ?>" class="form-control" data-toggle="summernote" data-lang="{{ summernote }}"><?php echo isset($jade_footer_copyright_description[$language['language_id']]) ? $jade_footer_copyright_description[$language['language_id']]['description'] : ''; ?></textarea>
                    </div>
                  </div>
                </div>
                <?php } ?>
              </div>
            </div>
            <div class="tab-pane" id="tab-links">
              <div class="form-group">
                <label class="col-sm-2 control-label"><?php echo $entry_link_sizeclass; ?></label>
                <div class="col-sm-10">
                  <select name="jade_footer_copyright_link_sizeclass" class="form-control">
                    <?php foreach($size_classes as $size_class_value) { ?>
                    <?php if($size_class_value['code'] == $jade_footer_copyright_link_sizeclass) { ?>
                    <option value="<?php echo $size_class_value['code']; ?>" selected="selected"><?php echo $size_class_value['title']; ?></option>
                    <?php } else { ?>
                    <option value="<?php echo $size_class_value['code']; ?>"><?php echo $size_class_value['title']; ?></option>
                    <?php } ?>
                    <?php } ?>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-2 control-label"><?php echo $entry_textalgin; ?></label>
                <div class="col-sm-5">
                  <div class="btn-group btn-group-toggle" data-toggle="buttons">
                    <label class="btn btn-success <?php echo $jade_footer_copyright_textalgin == 'left' ? 'active' : ''; ?>"><input type="radio" name="jade_footer_copyright_textalgin" value="left" <?php echo $jade_footer_copyright_textalgin == 'left' ? 'checked="checked"' : ''; ?> /> <?php echo $text_left; ?></label>

                    <label class="btn btn-success <?php echo $jade_footer_copyright_textalgin == 'center' ? 'active' : ''; ?>"><input type="radio" name="jade_footer_copyright_textalgin" value="center" <?php echo $jade_footer_copyright_textalgin == 'center' ? 'checked="checked"' : ''; ?> /> <?php echo $text_center; ?></label>

                    <label class="btn btn-success <?php echo $jade_footer_copyright_textalgin == 'right' ? 'active' : ''; ?>"><input type="radio" name="jade_footer_copyright_textalgin" value="right" <?php echo $jade_footer_copyright_textalgin == 'right' ? 'checked="checked"' : ''; ?> /> <?php echo $text_right; ?></label>
                  </div>
                </div>
              </div>
              <table id="informationlinks" class="table table-striped table-bordered table-hover">
                <thead>
                  <tr>
                    <td class="text-left required"><?php echo $entry_title; ?></td>
                    <td class="text-left"><?php echo $entry_url; ?></td>
                    <td class="text-right"><?php echo $entry_action; ?></td>
                  </tr>
                </thead>
                <tbody>
                  <?php $informationlinks_row = 0; ?>
                  <?php foreach ($informationlinks as $informationlink) { ?>
                  <tr id="informationlinks-row<?php echo $informationlinks_row; ?>">
                    <td class="text-left">
                      <?php foreach ($languages as $language) { ?>
                      <div class="input-group"><span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span>
                        <input type="text" name="jade_footer_copyright_informationlinks[<?php echo $informationlinks_row; ?>][informationlinks_description][<?php echo $language['language_id']; ?>][title]" value="<?php echo isset($informationlink['informationlinks_description'][$language['language_id']]['title']) ? $informationlink['informationlinks_description'][$language['language_id']]['title'] : ''; ?>" placeholder="<?php echo $entry_title; ?>" class="form-control" />
                      </div>
                      <?php if (isset($error_informationlinks[$informationlinks_row][$language['language_id']])) { ?>
                      <div class="text-danger"><?php echo $error_informationlinks[$informationlinks_row][$language['language_id']]; ?></div>
                      <?php } ?>
                      <?php } ?>
                    </td>
                    <td class="text-left"><input type="text" name="jade_footer_copyright_informationlinks[<?php echo $informationlinks_row; ?>][url]" value="<?php echo $informationlink['url']; ?>" class="form-control" /></td>
                    <td class="text-right"><button type="button" onclick="$('#informationlinks_row<?php echo $informationlinks_row; ?>').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>
                  </tr>
                  <?php $informationlinks_row++; ?>
                  <?php } ?>
                </tbody>
                <tfoot>
                  <tr>
                    <td colspan="2"></td>
                    <td class="text-right"><button type="button" onclick="addInformationLinks();" data-toggle="tooltip" title="<?php echo $button_informationlinks_add; ?>" class="btn btn-primary"><i class="fa fa-plus-circle"></i></button></td>
                  </tr>
                </tfoot>
              </table>
            </div>
            <div class="tab-pane" id="tab-colors">
              <div class="form-group">
                <label class="col-sm-2 control-label"><?php echo $entry_copyright_bg; ?></label>
                <div class="col-sm-3">
                  <div class="input-group colorpicker colorpicker-component">
                    <input type="text" name="jade_footer_copyright_bg" value="<?php echo $jade_footer_copyright_bg; ?>" class="form-control" />
                    <span class="input-group-addon"><i></i></span>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-2 control-label"><?php echo $entry_copyright_color; ?></label>
                <div class="col-sm-3">
                  <div class="input-group colorpicker colorpicker-component">
                    <input type="text" name="jade_footer_copyright_color" value="<?php echo $jade_footer_copyright_color; ?>" class="form-control" />
                    <span class="input-group-addon"><i></i></span>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-2 control-label"><?php echo $entry_copyright_links_color; ?></label>
                <div class="col-sm-3">
                  <div class="input-group colorpicker colorpicker-component">
                    <input type="text" name="jade_footer_copyright_links_color" value="<?php echo $jade_footer_copyright_links_color; ?>" class="form-control" />
                    <span class="input-group-addon"><i></i></span>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-2 control-label"><?php echo $entry_copyright_links_hover_color; ?></label>
                <div class="col-sm-3">
                  <div class="input-group colorpicker colorpicker-component">
                    <input type="text" name="jade_footer_copyright_links_hover_color" value="<?php echo $jade_footer_copyright_links_hover_color; ?>" class="form-control" />
                    <span class="input-group-addon"><i></i></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
<link href="view/javascript/codemirror/lib/codemirror.css" rel="stylesheet" />
<link href="view/javascript/codemirror/theme/monokai.css" rel="stylesheet" />
<script type="text/javascript" src="view/javascript/codemirror/lib/codemirror.js"></script>
<script type="text/javascript" src="view/javascript/codemirror/lib/xml.js"></script>
<script type="text/javascript" src="view/javascript/codemirror/lib/formatting.js"></script>
<script type="text/javascript" src="view/javascript/summernote/summernote.js"></script>
<link href="view/javascript/summernote/summernote.css" rel="stylesheet" />
<script type="text/javascript" src="view/javascript/summernote/summernote-image-attributes.js"></script>
<script type="text/javascript" src="view/javascript/summernote/opencart.js"></script>
<style type="text/css">
fieldset legend {
    color: #ff6666;
    font-weight: bold;
    margin-top: 30px;
    padding-bottom: 5px;
    text-transform: uppercase;
}
.notopmagin {
  margin-top: 0;
}
</style>

<script type="text/javascript"><!--
var informationlinks_row = <?php echo $informationlinks_row; ?>;

function addInformationLinks() {
  html  = '<tr id="informationlinks-row' + informationlinks_row + '">';
    html += '  <td class="text-left">';
  <?php foreach ($languages as $language) { ?>
  html += '    <div class="input-group">';
  html += '      <span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span><input type="text" name="jade_footer_copyright_informationlinks[' + informationlinks_row + '][informationlinks_description][<?php echo $language['language_id']; ?>][title]" value="" placeholder="<?php echo $entry_title; ?>" class="form-control" />';
    html += '    </div>';
  <?php } ?>
  html += '  </td>';
  html += '  <td class="text-left"><input type="text" name="jade_footer_copyright_informationlinks[' + informationlinks_row + '][url]" value="" placeholder="<?php echo $entry_url; ?>" class="form-control" /></td>';

  html += '  <td class="text-right"><button type="button" onclick="$(\'#informationlinks-row' + informationlinks_row + '\').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>';
  html += '</tr>';

  $('#informationlinks tbody').append(html);

  informationlinks_row++;
}
//--></script>
<script type="text/javascript"><!--
$(function() {
  $('.colorpicker').colorpicker();
});
//--></script>
<script type="text/javascript"><!--
$('#editor-language a:first').tab('show');
//--></script>
</div>
<?php echo $footer; ?>