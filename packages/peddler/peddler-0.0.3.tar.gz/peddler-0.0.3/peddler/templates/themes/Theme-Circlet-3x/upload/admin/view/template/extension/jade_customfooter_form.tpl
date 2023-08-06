<?php echo $header; ?><?php echo $column_left; ?>
<div id="content">
  <div class="page-header">
    <div class="container-fluid">
      <div class="pull-right">
        <button type="submit" form="form-customfooter" data-toggle="tooltip" title="<?php echo $button_save; ?>" class="btn btn-primary"><i class="fa fa-save"></i></button>
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
    <div class="panel panel-default">
      <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-pencil"></i> <?php echo $text_form; ?></h3>
      </div>
      <div class="panel-body">
        <form action="<?php echo $action; ?>" method="post" enctype="multipart/form-data" id="form-customfooter" class="form-horizontal">
          <ul class="nav nav-tabs">
            <li class="active"><a href="#tab-general" data-toggle="tab"><?php echo $tab_general; ?></a></li>
            <li><a href="#tab-data" data-toggle="tab"><?php echo $tab_data; ?></a></li>
            <li><a href="#tab-link" data-toggle="tab"><?php echo $tab_link; ?></a></li>
          </ul>
          <div class="tab-content">
            <div class="tab-pane active" id="tab-general">
              <div class="form-group required">
                <label class="col-sm-2 control-label"><?php echo $entry_title; ?></label>
                <div class="col-sm-10">
                  <?php foreach ($languages as $language) { ?>
                  <div class="input-group"><span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span>
                    <input type="text" name="jade_customfooter_description[<?php echo $language['language_id']; ?>][title]" value="<?php echo isset($jade_customfooter_description[$language['language_id']]['title']) ? $jade_customfooter_description[$language['language_id']]['title'] : ''; ?>" placeholder="<?php echo $entry_title; ?>" class="form-control" />
                  </div>
                  <?php if (isset($error_title[$language['language_id']])) { ?>
                  <div class="text-danger"><?php echo $error_title[$language['language_id']]; ?></div>
                  <?php } ?>
                  <?php } ?>
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-2 control-label" for="input-type"><?php echo $entry_type; ?></label>
                <div class="col-sm-10">
                  <select name="type_code" id="input-type" class="form-control">
                    <?php foreach($types as $type) { ?>
                    <?php if($type['code'] == $type_code) { ?>
                    <option value="<?php echo $type['code']; ?>" selected="selected"><?php echo $type['title']; ?></option>
                    <?php } else { ?>
                    <option value="<?php echo $type['code']; ?>"><?php echo $type['title']; ?></option>
                    <?php } ?>
                    <?php } ?>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-2 control-label" for="input-type"><?php echo $entry_size_class; ?></label>
                <div class="col-sm-10">
                  <select name="size_class" id="input-type" class="form-control">
                    <?php foreach($size_classes as $size_class_value) { ?>
                    <?php if($size_class_value['code'] == $size_class) { ?>
                    <option value="<?php echo $size_class_value['code']; ?>" selected="selected"><?php echo $size_class_value['title']; ?></option>
                    <?php } else { ?>
                    <option value="<?php echo $size_class_value['code']; ?>"><?php echo $size_class_value['title']; ?></option>
                    <?php } ?>
                    <?php } ?>
                  </select>
                </div>
              </div>
              <fieldset class="alltype type_contact_detail <?php echo $type_code == 'contact_detail' ? '' : 'hide'; ?>">
                <legend><?php echo $type_contact_detail; ?></legend>
                <table id="contactdetail" class="table table-striped table-bordered table-hover">
                  <thead>
                    <tr>
                      <td class="text-left required"><?php echo $entry_title; ?></td>
                      <td class="text-left"><?php echo $entry_icon; ?></td>
                      <td class="text-left"><?php echo $entry_url; ?></td>
                      <td class="text-right"><?php echo $entry_action; ?></td>
                    </tr>
                  </thead>
                  <tbody>
                    <?php $contactdetail_row = 0; ?>
                    <?php foreach ($contactdetail_tables as $contactdetail_table) { ?>
                    <tr id="contactdetail-row<?php echo $contactdetail_row; ?>">
                      <td class="text-left">
                        <?php foreach ($languages as $language) { ?>
                        <div class="input-group"><span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span>
                          <input type="text" name="contactdetail_table[<?php echo $contactdetail_row; ?>][contactdetail_description][<?php echo $language['language_id']; ?>][title]" value="<?php echo isset($contactdetail_table['contactdetail_description'][$language['language_id']]['title']) ? $contactdetail_table['contactdetail_description'][$language['language_id']]['title'] : ''; ?>" placeholder="<?php echo $entry_title; ?>" class="form-control" />
                        </div>
                        <?php if (isset($error_contactdetail[$contactdetail_row][$language['language_id']])) { ?>
                        <div class="text-danger"><?php echo $error_contactdetail[$contactdetail_row][$language['language_id']]; ?></div>
                        <?php } ?>
                        <?php } ?>
                      </td>
                      <td class="text-left"><input type="text" name="contactdetail_table[<?php echo $contactdetail_row; ?>][icon_class]" value="<?php echo $contactdetail_table['icon_class']; ?>" class="form-control" /></td>
                      <td class="text-left"><input type="text" name="contactdetail_table[<?php echo $contactdetail_row; ?>][url]" value="<?php echo $contactdetail_table['url']; ?>" class="form-control" /></td>
                      <td class="text-right"><button type="button" onclick="$('#contactdetail-row<?php echo $contactdetail_row; ?>').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>
                    </tr>
                    <?php $contactdetail_row++; ?>
                    <?php } ?>
                  </tbody>
                  <tfoot>
                    <tr>
                      <td colspan="3"></td>
                      <td class="text-right"><button type="button" onclick="addContactDetail();" data-toggle="tooltip" title="<?php echo $button_contactdetail_add; ?>" class="btn btn-primary"><i class="fa fa-plus-circle"></i></button></td>
                    </tr>
                  </tfoot>
                </table>
              </fieldset>
              <fieldset class="alltype type_newsletter <?php echo $type_code == 'newsletter' ? '' : 'hide'; ?>">
                <legend><?php echo $type_newsletter; ?></legend>
                <ul class="nav nav-tabs" id="newsletter-language">
                    <?php foreach ($languages as $language) { ?>
                    <li><a href="#newsletter-language<?php echo $language['language_id']; ?>" data-toggle="tab"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /> <?php echo $language['name']; ?></a></li>
                    <?php } ?>
                  </ul>
                  <div class="tab-content">
                    <?php foreach ($languages as $language) { ?>
                    <div class="tab-pane" id="newsletter-language<?php echo $language['language_id']; ?>">
                      <legend><?php echo $type_newsletter; ?></legend>
                      <div class="form-group required">
                        <label class="col-sm-2 control-label"><?php echo $entry_placeholder; ?></label>
                        <div class="col-sm-10">
                          <input type="text" name="newsletter_table[<?php echo $language['language_id']; ?>][placeholder]" placeholder="<?php echo $entry_placeholder; ?>" class="form-control" value="<?php echo isset($newsletter_table[$language['language_id']]['placeholder']) ? $newsletter_table[$language['language_id']]['placeholder'] : ''; ?>" />
                        </div>
                      </div>
                      <div class="form-group required">
                        <label class="col-sm-2 control-label"><?php echo $entry_button_text; ?></label>
                        <div class="col-sm-10">
                          <input type="text" name="newsletter_table[<?php echo $language['language_id']; ?>][button_text]" placeholder="<?php echo $entry_button_text; ?>" class="form-control" value="<?php echo isset($newsletter_table[$language['language_id']]['button_text']) ? $newsletter_table[$language['language_id']]['button_text'] : ''; ?>" />
                        </div>
                      </div>
                      <legend><?php echo $type_hotline; ?></legend>
                      <div class="form-group required">
                        <label class="col-sm-2 control-label"><?php echo $entry_hotline_title; ?></label>
                        <div class="col-sm-10">
                          <input type="text" name="newsletter_table[<?php echo $language['language_id']; ?>][hotline_title]" placeholder="<?php echo $entry_hotline_title; ?>" class="form-control" value="<?php echo isset($newsletter_table[$language['language_id']]['hotline_title']) ? $newsletter_table[$language['language_id']]['hotline_title'] : ''; ?>" />
                        </div>
                      </div>
                      <div class="form-group required">
                        <label class="col-sm-2 control-label"><?php echo $entry_hotline_description; ?></label>
                        <div class="col-sm-10">
                          <textarea name="newsletter_table[<?php echo $language['language_id']; ?>][hotline_description]" placeholder="<?php echo $entry_hotline_description; ?>" class="form-control" data-toggle="summernote" data-lang="{{ summernote }}"><?php echo isset($newsletter_table[$language['language_id']]['hotline_description']) ? $newsletter_table[$language['language_id']]['hotline_description'] : ''; ?></textarea>
                        </div>
                      </div>
                    </div>
                    <?php } ?>
                  </div>
              </fieldset>
              <fieldset class="alltype type_account_links <?php echo $type_code == 'account_links' ? '' : 'hide'; ?>">
                <legend><?php echo $type_account_links; ?></legend>
                <table id="accountlinks" class="table table-striped table-bordered table-hover">
                  <thead>
                    <tr>
                      <td class="text-left required"><?php echo $entry_title; ?></td>
                      <td class="text-left"><?php echo $entry_url; ?></td>
                      <td class="text-right"><?php echo $entry_action; ?></td>
                    </tr>
                  </thead>
                  <tbody>
                    <?php $accountlinks_row = 0; ?>
                    <?php foreach ($accountlinks_tables as $accountlinks_table) { ?>
                    <tr id="accountlinks-row<?php echo $accountlinks_row; ?>">
                      <td class="text-left">
                        <?php foreach ($languages as $language) { ?>
                        <div class="input-group"><span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span>
                          <input type="text" name="accountlinks_table[<?php echo $accountlinks_row; ?>][accountlinks_description][<?php echo $language['language_id']; ?>][title]" value="<?php echo isset($accountlinks_table['accountlinks_description'][$language['language_id']]['title']) ? $accountlinks_table['accountlinks_description'][$language['language_id']]['title'] : ''; ?>" placeholder="<?php echo $entry_title; ?>" class="form-control" />
                        </div>
                        <?php if (isset($error_accountlinks[$accountlinks_row][$language['language_id']])) { ?>
                        <div class="text-danger"><?php echo $error_accountlinks[$accountlinks_row][$language['language_id']]; ?></div>
                        <?php } ?>
                        <?php } ?>
                      </td>
                      <td class="text-left"><input type="text" name="accountlinks_table[<?php echo $accountlinks_row; ?>][url]" value="<?php echo $accountlinks_table['url']; ?>" class="form-control" /></td>
                      <td class="text-right"><button type="button" onclick="$('#accountlinks_row<?php echo $accountlinks_row; ?>').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>
                    </tr>
                    <?php $accountlinks_row++; ?>
                    <?php } ?>
                  </tbody>
                  <tfoot>
                    <tr>
                      <td colspan="2"></td>
                      <td class="text-right"><button type="button" onclick="addAccountLinks();" data-toggle="tooltip" title="<?php echo $button_accountlinks_add; ?>" class="btn btn-primary"><i class="fa fa-plus-circle"></i></button></td>
                    </tr>
                  </tfoot>
                </table>
              </fieldset>
              <fieldset class="alltype type_social_icons <?php echo $type_code == 'social_icons' ? '' : 'hide'; ?>">
                <legend><?php echo $type_social_icons; ?></legend>
                <table id="sociallinks" class="table table-striped table-bordered table-hover">
                  <thead>
                    <tr>
                      <td class="text-left required"><?php echo $entry_title; ?></td>
                      <td class="text-left"><?php echo $entry_url; ?></td>
                      <td class="text-left"><?php echo $entry_icon; ?></td>
                      <td class="text-right"><?php echo $entry_action; ?></td>
                    </tr>
                  </thead>
                  <tbody>
                    <?php $sociallinks_row = 0; ?>
                    <?php foreach ($sociallinks_tables as $sociallinks_table) { ?>
                    <tr id="sociallinks-row<?php echo $sociallinks_row; ?>">
                      <td class="text-left">
                        <?php foreach ($languages as $language) { ?>
                        <div class="input-group"><span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span>
                          <input type="text" name="sociallinks_table[<?php echo $sociallinks_row; ?>][sociallinks_description][<?php echo $language['language_id']; ?>][title]" value="<?php echo isset($sociallinks_table['sociallinks_description'][$language['language_id']]['title']) ? $sociallinks_table['sociallinks_description'][$language['language_id']]['title'] : ''; ?>" placeholder="<?php echo $entry_title; ?>" class="form-control" />
                        </div>
                        <?php if (isset($error_sociallinks[$sociallinks_row][$language['language_id']])) { ?>
                        <div class="text-danger"><?php echo $error_sociallinks[$sociallinks_row][$language['language_id']]; ?></div>
                        <?php } ?>
                        <?php } ?>
                      </td>
                      <td class="text-left"><input type="text" name="sociallinks_table[<?php echo $sociallinks_row; ?>][url]" value="<?php echo $sociallinks_table['url']; ?>" class="form-control" /></td>
                      <td class="text-left"><input type="text" name="sociallinks_table[<?php echo $sociallinks_row; ?>][icon_class]" value="<?php echo $sociallinks_table['icon_class']; ?>" class="form-control" /></td>
                      <td class="text-right"><button type="button" onclick="$('#sociallinks_row<?php echo $sociallinks_row; ?>').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>
                    </tr>
                    <?php $sociallinks_row++; ?>
                    <?php } ?>
                  </tbody>
                  <tfoot>
                    <tr>
                      <td colspan="3"></td>
                      <td class="text-right"><button type="button" onclick="addSocialLinks();" data-toggle="tooltip" title="<?php echo $button_sociallinks_add; ?>" class="btn btn-primary"><i class="fa fa-plus-circle"></i></button></td>
                    </tr>
                  </tfoot>
                </table>
              </fieldset>
              <fieldset class="alltype type_information_links <?php echo $type_code == 'information_links' ? '' : 'hide'; ?>">
                <legend><?php echo $type_information_links; ?></legend>
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
                    <?php foreach ($informationlinks_tables as $informationlinks_table) { ?>
                    <tr id="informationlinks-row<?php echo $informationlinks_row; ?>">
                      <td class="text-left">
                        <?php foreach ($languages as $language) { ?>
                        <div class="input-group"><span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span>
                          <input type="text" name="informationlinks_table[<?php echo $informationlinks_row; ?>][informationlinks_description][<?php echo $language['language_id']; ?>][title]" value="<?php echo isset($informationlinks_table['informationlinks_description'][$language['language_id']]['title']) ? $informationlinks_table['informationlinks_description'][$language['language_id']]['title'] : ''; ?>" placeholder="<?php echo $entry_title; ?>" class="form-control" />
                        </div>
                        <?php if (isset($error_informationlinks[$informationlinks_row][$language['language_id']])) { ?>
                        <div class="text-danger"><?php echo $error_informationlinks[$informationlinks_row][$language['language_id']]; ?></div>
                        <?php } ?>
                        <?php } ?>
                      </td>
                      <td class="text-left"><input type="text" name="informationlinks_table[<?php echo $informationlinks_row; ?>][url]" value="<?php echo $informationlinks_table['url']; ?>" class="form-control" /></td>
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
              </fieldset>
              <fieldset class="alltype type_payments_icons <?php echo $type_code == 'payments_icons' ? '' : 'hide'; ?>">
                <legend><?php echo $type_payments_icons; ?></legend>
                <table id="payments" class="table table-striped table-bordered table-hover">
                  <thead>
                    <tr>
                      <td class="text-left required"><?php echo $entry_title; ?></td>
                      <td class="text-left"><?php echo $entry_image; ?></td>
                      <td class="text-right"><?php echo $entry_action; ?></td>
                    </tr>
                  </thead>
                  <tbody>
                    <?php $payments_row = 0; ?>
                    <?php foreach ($payments_tables as $payments_table) { ?>
                    <tr id="payments-row<?php echo $payments_row; ?>">
                      <td class="text-left">
                        <?php foreach ($languages as $language) { ?>
                        <div class="input-group"><span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span>
                          <input type="text" name="payments_table[<?php echo $payments_row; ?>][payments_description][<?php echo $language['language_id']; ?>][title]" value="<?php echo isset($payments_table['payments_description'][$language['language_id']]['title']) ? $payments_table['payments_description'][$language['language_id']]['title'] : ''; ?>" placeholder="<?php echo $entry_title; ?>" class="form-control" />
                        </div>
                        <?php if (isset($error_payments[$payments_row][$language['language_id']])) { ?>
                        <div class="text-danger"><?php echo $error_payments[$payments_row][$language['language_id']]; ?></div>
                        <?php } ?>
                        <?php } ?>
                      </td>
                      <td class="text-left"><a href="" id="thumb-paymentimage<?php echo $payments_row; ?>" data-toggle="image" class="img-thumbnail"><img src="<?php echo $payments_table['thumb']; ?>" alt="" title="" data-placeholder="<?php echo $placeholder; ?>" /></a><input type="hidden" name="payments_table[<?php echo $payments_row; ?>][image]" value="<?php echo $payments_table['image']; ?>" id="input-paymentimage<?php echo $payments_row; ?>" /></td>
                      <td class="text-right"><button type="button" onclick="$('#payments-row<?php echo $payments_row; ?>').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>
                    </tr>
                    <?php $payments_row++; ?>
                    <?php } ?>
                  </tbody>
                  <tfoot>
                    <tr>
                      <td colspan="2"></td>
                      <td class="text-right"><button type="button" onclick="addPayments();" data-toggle="tooltip" title="<?php echo $button_payments_add; ?>" class="btn btn-primary"><i class="fa fa-plus-circle"></i></button></td>
                    </tr>
                  </tfoot>
                </table>
              </fieldset>
              <fieldset class="alltype type_app_icons <?php echo $type_code == 'app_icons' ? '' : 'hide'; ?>">
                <legend><?php echo $type_app_icons; ?></legend>
                <table id="appicons" class="table table-striped table-bordered table-hover">
                  <thead>
                    <tr>
                      <td class="text-left required"><?php echo $entry_title; ?></td>
                      <td class="text-left"><?php echo $entry_image; ?></td>
                      <td class="text-right"><?php echo $entry_action; ?></td>
                    </tr>
                  </thead>
                  <tbody>
                    <?php $appicons_row = 0; ?>
                    <?php foreach ($appicons_tables as $appicons_table) { ?>
                    <tr id="appicons-row<?php echo $appicons_row; ?>">
                      <td class="text-left">
                        <?php foreach ($languages as $language) { ?>
                        <div class="input-group"><span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span>
                          <input type="text" name="appicons_table[<?php echo $appicons_row; ?>][appicons_description][<?php echo $language['language_id']; ?>][title]" value="<?php echo isset($appicons_table['appicons_description'][$language['language_id']]['title']) ? $appicons_table['appicons_description'][$language['language_id']]['title'] : ''; ?>" placeholder="<?php echo $entry_title; ?>" class="form-control" />
                        </div>
                        <?php if (isset($error_appicons[$appicons_row][$language['language_id']])) { ?>
                        <div class="text-danger"><?php echo $error_appicons[$appicons_row][$language['language_id']]; ?></div>
                        <?php } ?>
                        <?php } ?>
                      </td>
                      <td class="text-left"><a href="" id="thumb-appiconsimage<?php echo $appicons_row; ?>" data-toggle="image" class="img-thumbnail"><img src="<?php echo $appicons_table['thumb']; ?>" alt="" title="" data-placeholder="<?php echo $placeholder; ?>" /></a><input type="hidden" name="appicons_table[<?php echo $appicons_row; ?>][image]" value="<?php echo $appicons_table['image']; ?>" id="input-appiconsimage<?php echo $appicons_row; ?>" /></td>
                      <td class="text-right"><button type="button" onclick="$('#appicons-row<?php echo $appicons_row; ?>').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>
                    </tr>
                    <?php $appicons_row++; ?>
                    <?php } ?>
                  </tbody>
                  <tfoot>
                    <tr>
                      <td colspan="2"></td>
                      <td class="text-right"><button type="button" onclick="addAppIcons();" data-toggle="tooltip" title="<?php echo $button_appicons_add; ?>" class="btn btn-primary"><i class="fa fa-plus-circle"></i></button></td>
                    </tr>
                  </tfoot>
                </table>
              </fieldset>
              <fieldset class="alltype type_editor <?php echo $type_code == 'editor' ? '' : 'hide'; ?>">
                <legend><?php echo $type_editor; ?></legend>
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
                          <textarea name="editor_description[<?php echo $language['language_id']; ?>][description]" placeholder="<?php echo $entry_description; ?>" id="input-editor-description<?php echo $language['language_id']; ?>" class="form-control" data-toggle="summernote" data-lang="{{ summernote }}"><?php echo isset($editor_description[$language['language_id']]) ? $editor_description[$language['language_id']]['description'] : ''; ?></textarea>
                        </div>
                      </div>
                    </div>
                    <?php } ?>
                  </div>
              </fieldset>
            </div>
            <div class="tab-pane" id="tab-data">
              <div class="form-group">
                <label class="col-sm-2 control-label" for="input-status"><?php echo $entry_status; ?></label>
                <div class="col-sm-10">
                  <select name="status" id="input-status" class="form-control">
                    <?php if ($status) { ?>
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
                <label class="col-sm-2 control-label" for="input-sort-order"><?php echo $entry_sort_order; ?></label>
                <div class="col-sm-10">
                  <input type="text" name="sort_order" value="<?php echo $sort_order; ?>" placeholder="<?php echo $entry_sort_order; ?>" id="input-sort-order" class="form-control" />
                </div>
              </div>
            </div>
            <div class="tab-pane" id="tab-link">
              <div class="form-group">
                <label class="col-sm-2 control-label"><?php echo $entry_customer_group; ?></label>
                <div class="col-sm-10">
                  <div class="well well-sm" style="height: 150px; overflow: auto;">
                    <?php foreach ($customer_groups as $customer_group) { ?>
                    <div class="checkbox">
                      <label>
                        <?php if (in_array($customer_group['customer_group_id'], $jade_customfooter_customer_group)) { ?>
                        <input type="checkbox" name="jade_customfooter_customer_group[]" value="<?php echo $customer_group['customer_group_id']; ?>" checked="checked" />
                        <?php echo $customer_group['name']; ?>
                        <?php } else { ?>
                        <input type="checkbox" name="jade_customfooter_customer_group[]" value="<?php echo $customer_group['customer_group_id']; ?>" />
                        <?php echo $customer_group['name']; ?>
                        <?php } ?>
                      </label>
                    </div>
                    <?php } ?>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-2 control-label"><?php echo $entry_store; ?></label>
                <div class="col-sm-10">
                  <div class="well well-sm" style="height: 150px; overflow: auto;">
                    <div class="checkbox">
                      <label>
                        <?php if (in_array(0, $jade_customfooter_store)) { ?>
                        <input type="checkbox" name="jade_customfooter_store[]" value="0" checked="checked" />
                        <?php echo $text_default; ?>
                        <?php } else { ?>
                        <input type="checkbox" name="jade_customfooter_store[]" value="0" />
                        <?php echo $text_default; ?>
                        <?php } ?>
                      </label>
                    </div>
                    <?php foreach ($stores as $store) { ?>
                    <div class="checkbox">
                      <label>
                        <?php if (in_array($store['store_id'], $jade_customfooter_store)) { ?>
                        <input type="checkbox" name="jade_customfooter_store[]" value="<?php echo $store['store_id']; ?>" checked="checked" />
                        <?php echo $store['name']; ?>
                        <?php } else { ?>
                        <input type="checkbox" name="jade_customfooter_store[]" value="<?php echo $store['store_id']; ?>" />
                        <?php echo $store['name']; ?>
                        <?php } ?>
                      </label>
                    </div>
                    <?php } ?>
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
<script type="text/javascript"><!--
// Type
$('select[name=\'type_code\']').on('change', function() {
  $('.alltype').addClass('hide');

  var menu_type = 'type_';
  $('.'+ menu_type + this.value).removeClass('hide');
});
//--></script>
<script type="text/javascript"><!--
// Language Tab
$('#editor-language a:first').tab('show');
$('#newsletter-language a:first').tab('show');
//--></script>
<script type="text/javascript"><!--
// Add Contact Detail
var contactdetail_row = <?php echo $contactdetail_row; ?>;

function addContactDetail() {
  html  = '<tr id="contactdetail-row' + contactdetail_row + '">';
    html += '  <td class="text-left">';
  <?php foreach ($languages as $language) { ?>
  html += '    <div class="input-group">';
  html += '      <span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span><input type="text" name="contactdetail_table[' + contactdetail_row + '][contactdetail_description][<?php echo $language['language_id']; ?>][title]" value="" placeholder="<?php echo $entry_title; ?>" class="form-control" />';
    html += '    </div>';
  <?php } ?>
  html += '  </td>';
  html += '  <td class="text-left"><input type="text" name="contactdetail_table[' + contactdetail_row + '][icon_class]" value="" placeholder="<?php echo $entry_icon; ?>" class="form-control" /></td>';
  html += '  <td class="text-left"><input type="text" name="contactdetail_table[' + contactdetail_row + '][url]" value="" placeholder="<?php echo $entry_url; ?>" class="form-control" /></td>';

  html += '  <td class="text-right"><button type="button" onclick="$(\'#contactdetail-row' + contactdetail_row + '\').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>';
  html += '</tr>';

  $('#contactdetail tbody').append(html);

  contactdetail_row++;
}
//--></script>

<script type="text/javascript"><!--
// Add Account Links
var accountlinks_row = <?php echo $accountlinks_row; ?>;

function addAccountLinks() {
  html  = '<tr id="accountlinks-row' + accountlinks_row + '">';
    html += '  <td class="text-left">';
  <?php foreach ($languages as $language) { ?>
  html += '    <div class="input-group">';
  html += '      <span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span><input type="text" name="accountlinks_table[' + accountlinks_row + '][accountlinks_description][<?php echo $language['language_id']; ?>][title]" value="" placeholder="<?php echo $entry_title; ?>" class="form-control" />';
    html += '    </div>';
  <?php } ?>
  html += '  </td>';
  html += '  <td class="text-left"><input type="text" name="accountlinks_table[' + accountlinks_row + '][url]" value="" placeholder="<?php echo $entry_url; ?>" class="form-control" /></td>';

  html += '  <td class="text-right"><button type="button" onclick="$(\'#accountlinks-row' + accountlinks_row + '\').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>';
  html += '</tr>';

  $('#accountlinks tbody').append(html);

  accountlinks_row++;
}
//--></script>

<script type="text/javascript"><!--
// Add Social Links
var sociallinks_row = <?php echo $sociallinks_row; ?>;

function addSocialLinks() {
  html  = '<tr id="sociallinks-row' + sociallinks_row + '">';
    html += '  <td class="text-left">';
  <?php foreach ($languages as $language) { ?>
  html += '    <div class="input-group">';
  html += '      <span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span><input type="text" name="sociallinks_table[' + sociallinks_row + '][sociallinks_description][<?php echo $language['language_id']; ?>][title]" value="" placeholder="<?php echo $entry_title; ?>" class="form-control" />';
    html += '    </div>';
  <?php } ?>
  html += '  </td>';
  html += '  <td class="text-left"><input type="text" name="sociallinks_table[' + sociallinks_row + '][url]" value="" placeholder="<?php echo $entry_url; ?>" class="form-control" /></td>';
  html += '  <td class="text-left"><input type="text" name="sociallinks_table[' + sociallinks_row + '][icon_class]" value="" placeholder="<?php echo $entry_icon; ?>" class="form-control" /></td>';
  html += '  <td class="text-right"><button type="button" onclick="$(\'#sociallinks-row' + sociallinks_row + '\').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>';
  html += '</tr>';

  $('#sociallinks tbody').append(html);

  sociallinks_row++;
}
//--></script>

<script type="text/javascript"><!--
// Add Information Links
var informationlinks_row = <?php echo $informationlinks_row; ?>;

function addInformationLinks() {
  html  = '<tr id="informationlinks-row' + informationlinks_row + '">';
    html += '  <td class="text-left">';
  <?php foreach ($languages as $language) { ?>
  html += '    <div class="input-group">';
  html += '      <span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span><input type="text" name="informationlinks_table[' + informationlinks_row + '][informationlinks_description][<?php echo $language['language_id']; ?>][title]" value="" placeholder="<?php echo $entry_title; ?>" class="form-control" />';
    html += '    </div>';
  <?php } ?>
  html += '  </td>';
  html += '  <td class="text-left"><input type="text" name="informationlinks_table[' + informationlinks_row + '][url]" value="" placeholder="<?php echo $entry_url; ?>" class="form-control" /></td>';

  html += '  <td class="text-right"><button type="button" onclick="$(\'#informationlinks-row' + informationlinks_row + '\').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>';
  html += '</tr>';

  $('#informationlinks tbody').append(html);

  informationlinks_row++;
}
//--></script>
<script type="text/javascript"><!--
// Add Payment Links
var payments_row = <?php echo $payments_row; ?>;

function addPayments() {
  html  = '<tr id="payments-row' + payments_row + '">';
    html += '  <td class="text-left">';
  <?php foreach ($languages as $language) { ?>
  html += '    <div class="input-group">';
  html += '      <span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span><input type="text" name="payments_table[' + payments_row + '][payments_description][<?php echo $language['language_id']; ?>][title]" value="" placeholder="<?php echo $entry_title; ?>" class="form-control" />';
    html += '    </div>';
  <?php } ?>
  html += '  </td>';
  html += '  <td class="text-left"><a href="" id="thumb-paymentimage' + payments_row + '"data-toggle="image" class="img-thumbnail"><img src="<?php echo $placeholder; ?>" alt="" title="" data-placeholder="<?php echo $placeholder; ?>" /></a><input type="hidden" name="payments_table[' + payments_row + '][image]" value="" id="input-paymentimage' + payments_row + '" /></td>';
  html += '  <td class="text-right"><button type="button" onclick="$(\'#payments-row' + payments_row + '\').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>';
  html += '</tr>';

  $('#payments tbody').append(html);

  payments_row++;
}
//--></script>
<script type="text/javascript"><!--
// Add App Icons
var appicons_row = <?php echo $appicons_row; ?>;

function addAppIcons() {
  html  = '<tr id="appicons-row' + appicons_row + '">';
    html += '  <td class="text-left">';
  <?php foreach ($languages as $language) { ?>
  html += '    <div class="input-group">';
  html += '      <span class="input-group-addon"><img src="language/<?php echo $language['code']; ?>/<?php echo $language['code']; ?>.png" title="<?php echo $language['name']; ?>" /></span><input type="text" name="appicons_table[' + appicons_row + '][appicons_description][<?php echo $language['language_id']; ?>][title]" value="" placeholder="<?php echo $entry_title; ?>" class="form-control" />';
    html += '    </div>';
  <?php } ?>
  html += '  </td>';
  html += '  <td class="text-left"><a href="" id="thumb-appiconsimage' + appicons_row + '"data-toggle="image" class="img-thumbnail"><img src="<?php echo $placeholder; ?>" alt="" title="" data-placeholder="<?php echo $placeholder; ?>" /></a><input type="hidden" name="appicons_table[' + appicons_row + '][image]" value="" id="input-appiconsimage' + appicons_row + '" /></td>';
  html += '  <td class="text-right"><button type="button" onclick="$(\'#appicons-row' + appicons_row + '\').remove();" data-toggle="tooltip" title="<?php echo $button_remove; ?>" class="btn btn-danger"><i class="fa fa-minus-circle"></i></button></td>';
  html += '</tr>';

  $('#appicons tbody').append(html);

  appicons_row++;
}
//--></script>
</div>
<?php echo $footer; ?>