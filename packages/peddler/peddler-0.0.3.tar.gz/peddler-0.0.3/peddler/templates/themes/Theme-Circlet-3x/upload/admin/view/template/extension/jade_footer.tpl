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
              <li><a href="#tab-colors" data-toggle="tab"><?php echo $tab_colors; ?></a></li>
              <li><a href="#tab-support" data-toggle="tab"><i class="fa fa-support"></i> <?php echo $tab_support; ?></a></li>
            </ul>
            <div class="tab-content">
              <div class="tab-pane active" id="tab-general">
                <fieldset>
                  <legend class=""><?php echo $text_control_panel; ?></legend>
                  <div class="form-group">
                    <label class="col-sm-2 control-label"><?php echo $entry_status; ?></label>
                    <div class="col-sm-3">
                      <select name="jade_footer_status" class="form-control">
                        <?php if ($jade_footer_status) { ?>
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
                    <label class="col-sm-2 control-label" for="input-logo"><?php echo $entry_logo; ?></label>
                    <div class="col-sm-10"><a href="" id="thumb-logo" data-toggle="image" class="img-thumbnail"><img src="<?php echo $logo; ?>" alt="" title="" data-placeholder="<?php echo $placeholder; ?>" /></a>
                      <input type="hidden" name="jade_footer_logo" value="<?php echo $jade_footer_logo; ?>" id="input-logo" />
                    </div>
                  </div>
                </fieldset>
              </div>
              <div class="tab-pane" id="tab-colors">
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_bgcolor; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_bgcolor" value="<?php echo $jade_footer_bgcolor; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_heading_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_heading_color" value="<?php echo $jade_footer_heading_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_icon_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_icon_color" value="<?php echo $jade_footer_icon_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_text_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_text_color" value="<?php echo $jade_footer_text_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_link_hover_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_link_hover_color" value="<?php echo $jade_footer_link_hover_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_social_media_bgcolor; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_social_media_bgcolor" value="<?php echo $jade_footer_social_media_bgcolor; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_social_media_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_social_media_color" value="<?php echo $jade_footer_social_media_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_social_media_hover_bgcolor; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_social_media_hover_bgcolor" value="<?php echo $jade_footer_social_media_hover_bgcolor; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_social_media_hover_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_social_media_hover_color" value="<?php echo $jade_footer_social_media_hover_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_newsletter_btn_bg; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_newsletter_btn_bg" value="<?php echo $jade_footer_newsletter_btn_bg; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_newsletter_btn_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_newsletter_btn_color" value="<?php echo $jade_footer_newsletter_btn_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_newsletter_input_border_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_newsletter_input_border_color" value="<?php echo $jade_footer_newsletter_input_border_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-2 control-label"><?php echo $entry_hot_line_color; ?></label>
                  <div class="col-sm-3">
                    <div class="input-group colorpicker colorpicker-component">
                      <input type="text" name="jade_footer_hot_line_color" value="<?php echo $jade_footer_hot_line_color; ?>" class="form-control" />
                      <span class="input-group-addon"><i></i></span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="tab-pane" id="tab-support">
                <div class="card-deck mb-3 text-center">
                  <div class="card mb-4 shadow-sm">
                    <div class="card-header">
                      <h4 class="my-0 font-weight-normal">Support</h4>
                    </div>
                    <div class="card-body">
                      <h4 class="card-title pricing-card-title">For Support Send E-mail at <big class="text-muted">extensionstudio.oc@gmail.com</big></h4>
                      <a target="_BLANK" href="https://www.opencart.com/index.php?route=marketplace/extension&filter_member=ExtensionStudio" class="btn btn-lg btn-primary">View Other Extensions</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
        </form>
      </div>
    </div>
  </div>
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
$(function() {
  $('.colorpicker').colorpicker();
});
//--></script>
</div>
<?php echo $footer; ?>